
async def receive_html(html_str: str | None = None):
    html = u'''
    <!DOCTYPE html>
    <html lang="en">
    {html_str}
    </html>'''
    return html