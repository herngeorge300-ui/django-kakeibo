from urllib import parse

from django.shortcuts import resolve_url

from django import template

register = template.Library()  # テンプレートライブラリに追加するための


@register.simple_tag
def get_return_link(request):
    """
    1つ前のページのURLをGET
    """
    top_page = resolve_url("kakeibo:cel_main")
    referer = request.environ.get("HTTP_REFERER")

    if referer:
        # 前のページのURLがあればそこに戻る
        parse_result = parse.urlparse(referer)
        if request.get_host() == parse_result.netloc:
            return referer
    # なければ
    print("WOWOWOWWOW")
    return top_page
