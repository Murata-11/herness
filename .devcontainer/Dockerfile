FROM mcr.microsoft.com/devcontainers/base:resolute

COPY --chmod=0755 drawio /usr/local/bin/drawio

RUN apt-get update \
    && drawio_version=32.6.10 \
    && arch="$(dpkg --print-architecture)" \
    && case "$arch" in \
        amd64) drawio_sha256=fc96faafe68cb4e06c0b7116779891592b20fce2cde7907adec504f23c5af83c ;; \
        arm64) drawio_sha256=3cd0b69b31f9113f09df43f47f149e78f1a109d628282ae713e13d0e5d320800 ;; \
        *) printf 'Unsupported draw.io architecture: %s\n' "$arch" >&2; exit 1 ;; \
    esac \
    && curl --fail --silent --show-error --location --retry 3 \
        --output /tmp/drawio.deb \
        "https://github.com/jgraph/drawio-desktop/releases/download/v${drawio_version}/drawio-${arch}-${drawio_version}.deb" \
    && printf '%s  /tmp/drawio.deb\n' "$drawio_sha256" | sha256sum --check \
    && apt-get install -y --no-install-recommends \
        /tmp/drawio.deb fonts-noto-cjk libasound2t64 python3-pymupdf xauth xvfb \
    && python3 -c 'import pymupdf' \
    && drawio --version \
    && rm -f /tmp/drawio.deb \
    && rm -rf /var/lib/apt/lists/*
