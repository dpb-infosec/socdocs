FROM alpine:latest AS hugo

ENV HUGO_VERSION 0.74.3
ENV GLIBC_VERSION 2.32-r0

RUN apk add --no-cache \
    bash \
    curl \
    git \
    libstdc++ \
    sudo

RUN wget  -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
&&  wget "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VERSION}/glibc-${GLIBC_VERSION}.apk" \
&&  apk --no-cache add "glibc-${GLIBC_VERSION}.apk" \
&&  rm "glibc-${GLIBC_VERSION}.apk" \
&&  wget "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VERSION}/glibc-bin-${GLIBC_VERSION}.apk" \
&&  apk --no-cache add "glibc-bin-${GLIBC_VERSION}.apk" \
&&  rm "glibc-bin-${GLIBC_VERSION}.apk" \
&&  wget "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VERSION}/glibc-i18n-${GLIBC_VERSION}.apk" \
&&  apk --no-cache add "glibc-i18n-${GLIBC_VERSION}.apk" \
&&  rm "glibc-i18n-${GLIBC_VERSION}.apk"
