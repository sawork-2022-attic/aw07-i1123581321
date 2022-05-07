package com.micropos.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
@EnableDiscoveryClient
public class GatewayApplication {
    private static final String PRODUCT = "lb://product-service";
    private static final String CART = "lb://cart-service";

    private static final String ORDER = "lb://order-service";

    private static final String DELIVERY = "lb://delivery-service";

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }

    @Bean
    public RouteLocator route(RouteLocatorBuilder builder){
        return builder.routes()
                .route(p -> p.path("/products/**")
                        .filters(f -> f.stripPrefix(1))
                        .uri(PRODUCT))
                .route(p -> p.path("/carts/**")
                        .filters(f -> f.stripPrefix(1))
                        .uri(CART))
                .route(p -> p.path("/orders/**")
                        .filters(f -> f.stripPrefix(1))
                        .uri(ORDER))
                .route(p -> p.path("/waybills/**")
                        .filters(f -> f.stripPrefix(1))
                        .uri(DELIVERY))
                .build();
    }
}
