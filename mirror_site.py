#!/usr/bin/env python3
"""Create a browsable static mirror of public topstanki.ru pages.
Requires requests and beautifulsoup4. No WordPress database or checkout is copied.
"""
import os, re, time, hashlib
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit, unquote
import requests
from bs4 import BeautifulSoup

ROOT="https://topstanki.ru/"
OUT=Path("mirror")
MAX_PAGES=int(os.getenv("MAX_PAGES","220"))
MAX_ASSETS=int(os.getenv("MAX_ASSETS","1400"))
MAX_BYTES=int(os.getenv("MAX_BYTES","180000000"))
TIMEOUT=18
session=requests.Session()
session.headers.update({"User-Agent":"Topstanki-site-archiver/1.0 (+static editorial backup)"})
pages=deque([ROOT,"https://topstanki.ru/karta-sajta-topstanki-dlya-poiskovikov/"])
visited=set()
assets={}
bytes_downloaded=0

def canonical(url):
    s=urlsplit(urljoin(ROOT,url))
    if s.scheme not in ("http","https") or s.hostname not in ("topstanki.ru","www.topstanki.ru"):return None
    path=re.sub(r"/+","/",s.path or "/")
    if path.startswith(("/wp-admin/","/wp-json/","/cart/","/checkout/","/my-account/")):return None
    if re.search(r"\.(zip|rar|exe|mp4|webm|pdf|docx?|xlsx?)$",path,re.I):return None
    if s.query and any(x in s.query for x in ("add-to-cart","wc-ajax","rest_route","preview=")):return None
    return urlunsplit(("https","topstanki.ru",path,"",""))

def page_path(url):
    p=unquote(urlsplit(url).path)
    if p.endswith(".html"):return OUT/p.lstrip("/")
    if re.search(r"\.[a-z0-9]{2,5}$",p,re.I):return OUT/(p.lstrip("/")+".html")
    return OUT/p.lstrip("/")/"index.html"

def fetch(url):
    global bytes_downloaded
    if bytes_downloaded>=MAX_BYTES:return None
    try:
        r=session.get(url,timeout=TIMEOUT)
        r.raise_for_status()
        size=len(r.content)
        if bytes_downloaded+size>MAX_BYTES:return None
        bytes_downloaded+=size
        return r
    except requests.RequestException as e:
        print("SKIP",url,str(e)[:90]);return None

def asset_path(url):
    s=urlsplit(url)
    ext=Path(s.path).suffix.lower()
    if not ext or len(ext)>7:ext=".bin"
    if s.hostname in ("topstanki.ru","www.topstanki.ru"):
        p=unquote(s.path).lstrip("/")
        if not p:p="asset"+ext
        if s.query:p+="-"+hashlib.sha1(s.query.encode()).hexdigest()[:8]+ext
        return OUT/"assets"/p
    h=hashlib.sha1(url.encode()).hexdigest()[:18]
    return OUT/"assets"/"external"/(h+ext)

def download_asset(url):
    if url in assets:return assets[url]
    if len(assets)>=MAX_ASSETS:return url
    s=urlsplit(url)
    if s.scheme not in ("http","https"):return url
    if s.path.endswith((".php",)) or "/wp-json/" in s.path:return url
    r=fetch(url)
    if r is None:return url
    typ=r.headers.get("content-type","").lower()
    if "text/html" in typ:return url
    dest=asset_path(url);dest.parent.mkdir(parents=True,exist_ok=True)
    data=r.content
    if "text/css" in typ or dest.suffix.lower()==".css":
        css=r.text
        def repl(m):
            raw=m.group(2).strip()
            if raw.startswith(("data:","#","blob:")):return m.group(0)
            new=download_asset(urljoin(url,raw))
            return 'url("'+("../"*len(dest.relative_to(OUT).parts[:-1]))+str(new.relative_to(OUT))+'")' if isinstance(new,Path) else m.group(0)
        # Mark asset before recursive CSS imports
        assets[url]=dest
        css=re.sub(r'url\(\s*([\'"]?)([^)\'"]+)\1\s*\)',repl,css)
        data=css.encode("utf-8")
    dest.write_bytes(data);assets[url]=dest
    return dest

def relative(from_path,to_path):
    return os.path.relpath(str(to_path),start=str(from_path.parent)).replace(os.sep,"/")

def html_page(url):
    r=fetch(url)
    if r is None or "html" not in r.headers.get("content-type",""):return False
    soup=BeautifulSoup(r.content,"html.parser")
    dest=page_path(url)
    dest.parent.mkdir(parents=True,exist_ok=True)
    for tag in soup.find_all(True):
        for attr in ("href","src","poster","data-src","data-bg","data-lazy-src"):
            raw=tag.get(attr)
            if not isinstance(raw,str) or not raw or raw.startswith(("#","data:","javascript:","mailto:","tel:")):continue
            full=urljoin(url,raw)
            if attr=="href" and tag.name=="a":
                clean=canonical(full)
                if clean:
                    if clean not in visited:pages.append(clean)
                    tag[attr]=relative(dest,page_path(clean))
                continue
            if tag.name=="link" and attr=="href" and (tag.get("rel") and any(x in tag.get("rel",[]) for x in ("stylesheet","icon","preload"))):
                pass
            elif attr=="href":continue
            if attr in ("src","poster","data-src","data-bg","data-lazy-src","href"):
                local=download_asset(full)
                if isinstance(local,Path):tag[attr]=relative(dest,local)
        for attr in ("srcset","data-srcset"):
            value=tag.get(attr)
            if not value:continue
            pieces=[]
            for item in value.split(","):
                entry=item.strip().split()
                if not entry:continue
                local=download_asset(urljoin(url,entry[0]))
                pieces.append(" ".join([relative(dest,local) if isinstance(local,Path) else entry[0]]+entry[1:]))
            tag[attr]=", ".join(pieces)
    for tag in soup.select('script[src*="yandex"],script[src*="google-analytics"],script[src*="googletagmanager"]'):
        tag.decompose()
    # Archive is informational: checkout/search/forms still need backend.
    notice=soup.new_tag("div",attrs={"id":"mirror-notice"})
    notice["style"]="background:#155c39;color:#fff;padding:9px 18px;text-align:center;font:14px Arial,sans-serif;position:relative;z-index:99999"
    notice.string="Архивная редактируемая копия ТОПСТАНКИ. Покупка, поиск и формы требуют подключения серверной части."
    if soup.body:soup.body.insert(0,notice)
    dest.write_text(str(soup),encoding="utf-8")
    print("PAGE",url, "=>", dest)
    return True

def main():
    OUT.mkdir(exist_ok=True)
    while pages and len(visited)<MAX_PAGES and bytes_downloaded<MAX_BYTES:
        url=pages.popleft()
        if url in visited:continue
        visited.add(url)
        html_page(url)
        time.sleep(.15)
    Path("index.html").write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=mirror/index.html"><title>ТОПСТАНКИ</title><a href="mirror/index.html">Открыть копию</a></html>',encoding="utf-8")
    print(f"DONE: {len(visited)} page URLs, {len(assets)} assets, {bytes_downloaded/1e6:.1f} MB. Output in mirror/")
if __name__=="__main__":main()
