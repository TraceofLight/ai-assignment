"""공개 HTTP 서비스의 실제 응답을 검사한다. 외부 Python 패키지 불필요."""
import sys
import urllib.request


def verify(base_url):
    # 사용자 PC에서 실행해 VM 내부 검사와 구분한다. 시스템 프록시는 사용하지 않는다.
    client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with client.open(base_url.rstrip('/') + '/health', timeout=10) as response:
        body = response.read()
        if response.status != 200 or body != b'OK':
            raise AssertionError(f'health 응답 불일치: {response.status}, {body!r}')
        print(f'PASS {response.url}: {response.status}, body={body!r}')
    with client.open(base_url.rstrip('/') + '/', timeout=10) as response:
        if response.status != 200 or b'HELLO CLOUD' not in response.read():
            raise AssertionError('웹 페이지 응답 불일치')
        print(f'PASS {response.url}: {response.status}, HELLO CLOUD')


if __name__ == '__main__':
    verify(sys.argv[1] if len(sys.argv) > 1 else 'http://152.67.213.106')
