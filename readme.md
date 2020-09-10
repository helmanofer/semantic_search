 run elasticsearch:
 
    sudo docker run -p 9200:9200 -p 9600:9600 \
    -e "discovery.type=single-node" \
    -e "opendistro_security.ssl.http.enabled=false" \ 
    amazon/opendistro-for-elasticsearch:1.9.0