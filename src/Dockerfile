FROM public.ecr.aws/lambda/provided:al2 as build

WORKDIR /asset

# install compiler
RUN yum install -y golang

RUN go env -w GOPROXY=direct

# cache dependencies
ADD go.mod go.sum ./

RUN go mod download

# build
ADD . .

RUN go build -tags lambda.norpc -o bootstrap

RUN ls -l

# copy artifacts to a clean image
FROM public.ecr.aws/lambda/provided:al2

WORKDIR /asset

COPY --from=build asset/bootstrap bootstrap

ENTRYPOINT [ "/boostrap" ]           