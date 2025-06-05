$(document).ready(function () {
    // Agregar Producto
    $("#agregar-producto").on("click", function () {
        $.ajax({
            type: "POST",
            url: "/agregar_producto/",
            data: {
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                producto_id: $("#producto_id").val(),
                cantidad: $("#cantidad").val(),
                pedido_id: $("#nro_pedido").val()
            },
            success: function (response) {
                if (response.success) {
                    $("#productos-solicitados").html(response.html);
                    alert("Producto agregado correctamente.");
                } else {
                    alert("Error: " + response.error);
                }
            },
            error: function () {
                alert("Error al agregar el producto.");
            }
        });
    });

    // Guardar Pedido
    $("#guardar-pedido").on("click", function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "/guardar_pedido/",
            data: $("#pedido-form").serialize(),
            success: function (response) {
                if (response.success) {
                    alert("Pedido guardado correctamente.");
                    window.location.href = "/ver_pedidos/"; // Redirigir a la vista ver_pedidos
                } else {
                    alert("Error: " + response.error);
                }
            },
            error: function () {
                alert("Error al guardar el pedido.");
            }
        });
    });
});