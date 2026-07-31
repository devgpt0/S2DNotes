FROM node:22-bookworm-slim

WORKDIR /workspace

RUN corepack enable

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/web/package.json ./apps/web/package.json
RUN pnpm install --frozen-lockfile --filter @genius/web...

COPY apps/web ./apps/web
WORKDIR /workspace/apps/web
RUN pnpm build

ENV NODE_ENV=production
ENV PORT=3000

RUN mkdir -p /data

EXPOSE 3000

CMD ["pnpm", "start"]
