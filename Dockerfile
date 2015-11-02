FROM eavatar/basebox
MAINTAINER sampot <sam@eavatar.com>

ADD dist/avame /avame
# RUN chown -R ava:ava /avame
EXPOSE 5080 5443
# ENTRYPOINT ["/avame/avame"]
CMD ["/avame/avame"]