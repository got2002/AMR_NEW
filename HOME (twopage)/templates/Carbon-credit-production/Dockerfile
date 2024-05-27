FROM node:16.14.2-alpine3.14 as builder

WORKDIR /usr/src/nuxt-app

COPY . .

RUN yarn install \
  --prefer-offline \
  --frozen-lockfile \
  --non-interactive \
  --production=false

ARG BASE_URL
ENV BASE_URL ${BASE_URL}

RUN yarn build

RUN rm -rf node_modules && \
  NODE_ENV=production yarn install \
  --prefer-offline \
  --pure-lockfile \
  --non-interactive \
  --production=true


FROM node:16.14.2-alpine3.14

WORKDIR /usr/src/nuxt-app

COPY --from=builder /usr/src/nuxt-app  .

ARG BASE_URL
ENV BASE_URL ${BASE_URL}

RUN yarn generate

ENV HOST 0.0.0.0
EXPOSE 3000

CMD [ "yarn", "start" ]


# # Dockerfile
# FROM node:16.14.2-alpine3.14

# # create destination directory
# RUN mkdir -p /usr/src/nuxt-app
# WORKDIR /usr/src/nuxt-app

# # update and install dependency
# RUN apk update && apk upgrade
# RUN apk add git

# # copy the app, note .dockerignore
# COPY . /usr/src/nuxt-app/

# ARG BASE_URL2

# ENV BASE_URL2 ${BASE_URL2}

# RUN npm install
# RUN yarn build



# EXPOSE 3000

# ENV NUXT_HOST=0.0.0.0
# ENV NUXT_PORT=3000

# CMD [ "npm", "run", "start" ]