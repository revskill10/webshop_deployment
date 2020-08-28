FROM odoo:11
MAINTAINER Dung <info@odoo.com>
USER root
RUN pip3 install cloudinary unidecode
USER odoo
COPY ./addons /mnt/extra-addons
COPY ./config/odoo/conf /etc/odoo/conf/odoo.conf

