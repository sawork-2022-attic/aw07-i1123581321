package com.micropos.cart.mapper;

import com.micropos.cart.model.Cart;
import com.micropos.cart.model.Item;
import com.micropos.dto.CartDto;
import com.micropos.dto.CartItemDto;
import com.micropos.dto.ProductDto;
import org.mapstruct.Mapper;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

@Mapper
public interface CartMapper {
    Collection<CartDto> toCartDtos(Collection<Cart> carts);

    Collection<Cart> toCarts(Collection<CartDto> cartDtos);

    default Cart toCart(CartDto cartDto) {
        return new Cart(cartDto.getId(),
                toItems(cartDto.getItems(), cartDto));

    }

    default CartDto toCartDto(Cart cart) {
        return new CartDto().id(cart.getId())
                .items(toItemDtos(cart.getItems()));
    }


    default List<CartItemDto> toItemDtos(List<Item> items) {
        if (items == null || items.isEmpty()) {
            return null;
        }
        List<CartItemDto> list = new ArrayList<>(items.size());
        for (Item item : items) {
            list.add(toItemDto(item));
        }

        return list;
    }

    default List<Item> toItems(List<CartItemDto> itemDtos, CartDto cartDto) {
        if (itemDtos == null || itemDtos.isEmpty()) {
            return null;
        }
        List<Item> list = new ArrayList<>(itemDtos.size());
        for (CartItemDto itemDto : itemDtos) {
            list.add(toItem(itemDto, cartDto));
        }

        return list;
    }

    default CartItemDto toItemDto(Item item) {

        return new CartItemDto().id(item.getId())
                .amount(item.getQuantity())
                .product(getProductDto(item));
    }

    default Item toItem(CartItemDto itemDto, CartDto cartDto) {
        return new Item(
                itemDto.getId(),
                cartDto.getId(),
                itemDto.getProduct().getId(),
                itemDto.getProduct().getName(),
                itemDto.getProduct().getPrice(),
                itemDto.getAmount());
    }

    default ProductDto getProductDto(Item item) {
        return new ProductDto().id(item.getProductId())
                .name(item.getProductName())
                .price(item.getUnitPrice());
    }

}
