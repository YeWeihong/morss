FROM alpine:edge

ADD . /app

RUN set -ex; \
	apk add --no-cache --virtual .run-deps python3 py3-lxml py3-setproctitle py3-setuptools; \
	apk add --no-cache --virtual .build-deps py3-pip py3-wheel; \
    # ↓↓↓ 修改了下面这一行，增加了 --break-system-packages 参数 ↓↓↓
	pip3 install --no-cache-dir --break-system-packages /app[full]; \
	apk del .build-deps

# 使用root用户权限，可以避免缓存文件权限不足的问题
# USER 1000:1000

ENTRYPOINT ["/bin/sh", "/app/morss-helper"]
CMD ["run"]

HEALTHCHECK CMD /bin/sh /app/morss-helper check
