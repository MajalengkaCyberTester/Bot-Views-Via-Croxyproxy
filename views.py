import sys
import asyncio
import re
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from asyncio import Lock
from argparse import ArgumentParser

WATCH_DURATION = 30  # default detik
MAX_WORKERS = 5       # default thread
console = Console()
thread_status = {}
thread_proxy = {}
thread_locks = {}
thread_watch_timer = {}

def fixed_len(text, length=25):
    return text.ljust(length)[:length]

def render_layout():
    layout = Layout()
    layout.split_column(
        Layout(Panel(Align.center("[bold cyan]\U0001FAB0 Trafix Views via CroxyProxy Dinamis[/bold cyan]"), border_style="bright_magenta")),
        Layout(render_table())
    )
    return layout

def render_table():
    table = Table(show_header=True, header_style="bold blue", expand=False)
    table.add_column("Thread", style="bold yellow", min_width=10, max_width=10)
    table.add_column("Status", style="white", min_width=30, max_width=35, overflow="ellipsis")
    table.add_column("Proxy", style="green", min_width=15, max_width=20, overflow="ellipsis")

    for tid in sorted(thread_status.keys()):
        status = thread_status.get(tid, "⏳")
        proxy = thread_proxy.get(tid, "⏳ Mendeteksi...")

        if tid in thread_watch_timer:
            elapsed = thread_watch_timer[tid]
            if elapsed > 0:
                total_m = WATCH_DURATION // 60
                total_s = WATCH_DURATION % 60
                total_str = f"{total_m}m" if total_s == 0 else f"{total_m}m{total_s}s" if total_m > 0 else f"{WATCH_DURATION}s"

                if elapsed < 60:
                    elapsed_str = f"{elapsed}s"
                else:
                    m, s = divmod(elapsed, 60)
                    elapsed_str = f"{m}m{s:02d}s"

                status = fixed_len(f"[Play] {elapsed_str} / {total_str}", 35)

        table.add_row(tid, fixed_len(status, 35), proxy)

    return table

async def get_croxyproxy_final_url(youtube_url, thread_id):
    async with thread_locks[thread_id]:
        thread_status[thread_id] = fixed_len("[Form] CroxyProxy")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        final_ip_url = None

        async def capture_request(route, request):
            nonlocal final_ip_url
            url = request.url
            if "watch?v=" in url and any(c.isdigit() for c in url.split("/")[2]):
                final_ip_url = url
            await route.continue_()

        await context.route("**/*", capture_request)
        await page.goto("https://www.croxyproxy.com", timeout=60000)
        await page.fill("input[name='url']", youtube_url)
        await page.click("button#requestSubmit")

        async with thread_locks[thread_id]:
            thread_status[thread_id] = fixed_len("[Wait] IP publik...")

        for _ in range(30):
            if final_ip_url:
                break
            await asyncio.sleep(1)

        await browser.close()

        if final_ip_url:
            parsed = urlparse(final_ip_url)
            domain = parsed.hostname or "unknown"
            async with thread_locks[thread_id]:
                thread_proxy[thread_id] = domain
                if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
                    thread_status[thread_id] = fixed_len(f"IP: {domain}")
                else:
                    thread_status[thread_id] = fixed_len(f"Proxy: {domain}")
            return final_ip_url
        else:
            async with thread_locks[thread_id]:
                thread_status[thread_id] = fixed_len("[Fail] Tidak ada IP")
                thread_proxy[thread_id] = "-"
            return None

async def watch_video(proxied_url, thread_id):
    async with thread_locks[thread_id]:
        thread_status[thread_id] = fixed_len("[Open] Memutar video")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(proxied_url, timeout=90000)
            await page.wait_for_timeout(5000)
            await page.evaluate("""() => {
                const vid = document.querySelector("video");
                if (vid) vid.play();
            }""")
            async with thread_locks[thread_id]:
                thread_status[thread_id] = fixed_len("[Play] Menonton...")
        except Exception:
            async with thread_locks[thread_id]:
                thread_status[thread_id] = fixed_len("[Err] Gagal play")
            await browser.close()
            return

        for elapsed in range(1, WATCH_DURATION + 1):
            thread_watch_timer[thread_id] = elapsed
            await asyncio.sleep(1)

        await browser.close()
        async with thread_locks[thread_id]:
            thread_watch_timer[thread_id] = 0
            thread_status[thread_id] = fixed_len("[Done] Selesai nonton")

async def session_worker(thread_id, youtube_url):
    while True:
        async with thread_locks[thread_id]:
            thread_status[thread_id] = fixed_len("[Init] Mulai sesi")

        try:
            final_url = await get_croxyproxy_final_url(youtube_url, thread_id)
            if final_url:
                await watch_video(final_url, thread_id)
            else:
                async with thread_locks[thread_id]:
                    thread_status[thread_id] = fixed_len("[Wait] Retry")
                await asyncio.sleep(10)
        except Exception as e:
            async with thread_locks[thread_id]:
                thread_status[thread_id] = fixed_len(f"[Err] {str(e)[:22]}")
        await asyncio.sleep(3)

async def main(youtube_url, total_threads):
    for i in range(1, total_threads + 1):
        tid = f"Thread {i}"
        thread_status[tid] = fixed_len("[Ready] Siap")
        thread_proxy[tid] = "-"
        thread_locks[tid] = Lock()
        thread_watch_timer[tid] = 0
        asyncio.create_task(session_worker(tid, youtube_url))

    with Live(render_layout(), refresh_per_second=2, screen=False, console=console) as live:
        while True:
            live.update(render_layout())
            await asyncio.sleep(1)

def parse_args():
    parser = ArgumentParser(description="YouTube View via CroxyProxy")
    parser.add_argument("youtube_url", help="URL YouTube yang ingin ditonton")
    parser.add_argument("--durasi", type=int, default=0, help="Durasi nonton dalam menit (opsional)")
    parser.add_argument("--threads", type=int, default=0, help="Jumlah thread yang berjalan paralel")

    args = parser.parse_args()

    global WATCH_DURATION, MAX_WORKERS

    if args.durasi > 0:
        WATCH_DURATION = args.durasi * 60  # menit ke detik

    if args.threads > 0:
        MAX_WORKERS = args.threads

    return args

if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(main(args.youtube_url, MAX_WORKERS))
    except KeyboardInterrupt:
        print("\n[❗] Dihentikan oleh pengguna.")
