FROM eavatar/basebox
MAINTAINER sampot <sam@eavatar.com>

ADD dist/avame /avame
# RUN chown -R ava:ava /avame
EXPOSE 5080 5443
# ENTRYPOINT ["/avame/avame"]
ENV AVA_POD /home/ava/.config/avame
# CMD ["/usr/bin/chpst", "-u", "ava:ava", "-U", "ava:ava", "/avame/avame"]
USER ava
CMD ["/avame/avame"]