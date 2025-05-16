FROM ubuntu:noble

WORKDIR /app

RUN apt-get update -y && apt-get install -y gnuplot rt-tests

COPY histogram-plot.sh /app/
RUN chmod +x histogram-plot.sh

CMD ["./histogram-plot.sh"]
