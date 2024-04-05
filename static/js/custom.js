var inputUrl = new URL(window.location.href);
var inputParams = new URLSearchParams(inputUrl.search);

function updateInputUrlAndInputParams() {
    inputUrl = new URL(window.location.href);
    inputParams = new URLSearchParams(inputUrl.search);
};

function setParameter(name, value) {
    let inputUrl = new URL(window.location.href);
    let inputParams = new URLSearchParams(inputUrl.search);

    inputParams.set(name, value);
    window.location.assign(inputUrl.href.split("?")[0] + "?" + inputParams);
};

function deleteParameter(name) {
    let inputUrl = new URL(window.location.href);
    let inputParams = new URLSearchParams(inputUrl.search);

    inputParams.delete(name)
    window.location.assign(inputUrl.href.split("?")[0] + "?" + inputParams);
};

function setParameterWithOutReload(name, value) {
    updateInputUrlAndInputParams()
    inputParams.set(name, value)
    var url = inputUrl.href.split("?")[0] + "?" + inputParams
    window.history.pushState("", "", url);
};

function deleteParameterWithOutReload(name) {
    updateInputUrlAndInputParams()
    inputParams.delete(name)
    var url = inputUrl.href.split("?")[0] + "?" + inputParams
    window.history.pushState("", "", url);
};

function separate(number) {
    return (number).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            };
        };
    };
    return cookieValue;
};

function setProductFilter(data, productFilterUrl) {
    for (let key in data) {
        setParameterWithOutReload(key, data[key])
    };
    var paramData = {};
    updateInputUrlAndInputParams();

    for (let [key, value] of inputParams) {
        paramData[key] = value;
    };

    if ("paginate_change" in paramData) {
        deleteParameterWithOutReload("page")
    }

    deleteParameterWithOutReload("category_change");
    deleteParameterWithOutReload("in_stock_change");
    deleteParameterWithOutReload("paginate_change");

    $.get(productFilterUrl, paramData).then(res => {
        if (res["categories"]) {
            $("#category-area").html(res["categories"]);
        } else if (res["paginates"]) {
            $(".paginate").html(res["paginates"]);
        };
        $("#products-area").html(res["products"]);
        $(".pagination").html(res["pagination"]);
        $("#price-filter-area").html(res["price_filter"]);
        $.getScript("/static/js/main.js")
    });
};

function productInStockFilter() {
    var isChecked = document.getElementById("toggle-switch-checkbox").checked;
    if (isChecked) {
        setProductFilter({ "in_stock": "true", "in_stock_change": "true" }, "/products/filter")
    } else {
        setProductFilter({ "in_stock": "false", "in_stock_change": "true" }, "/products/filter")
    };
};

function replyComment(parentId, userName) {
    document.getElementById("parentId").value = parentId;
    document.getElementById("myTab").scrollIntoView({ behavior: "smooth" });
    var comment = document.getElementById("commentText");
    comment.focus();
    comment.placeholder = `پاسخ برای نظر ${userName}`
};

function removeComment(commentId) {
    Swal.fire({
        title: "مطمئنی؟",
        icon: "warning",
        showCancelButton: true,
        focusCancel: true,
        confirmButtonText: "حذف",
        cancelButtonText: "متوقف کردن",
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
    }).then((result) => {
        if (result.isConfirmed) {
            $.get("/products/remove-comment", {
                comment_id: commentId
            }).then(res => {
                if (res["error"]) {
                    Swal.fire({
                        position: "center",
                        icon: "error",
                        title: res["error"],
                        showConfirmButton: false,
                        timer: 1500
                    });
                } else {
                    commentListArea = res["comment_list_area"];
                    $("#comment-list-area").html(commentListArea);
                    showAlert("نظر با موفقیت حذف شد", "success", "top-end")
                };
            });
        };
    });
};

function changeCommentStatus(commentId) {
    $.get("/products/change-comment-status", {
        comment_id: commentId
    }).then(res => {
        var error = res["error"]
        if (error) {
            Swal.fire({
                position: "center",
                icon: "error",
                title: error,
                showConfirmButton: false,
                timer: 1500
            });
        } else {
            var currentStatus = res["current_status"];
            $(`#comment-${commentId}-status`).html(currentStatus);
            showAlert(`وضعیت نظر به ${currentStatus} تغییر یافت`, "success", "top-end")
        };
    });
};

function setStockMessage(stockCount) {
    var message;
    if (stockCount > 5) {
        message = "موجود است";
    } else if (stockCount > 0) {
        message = `تنها ${stockCount} عدد در انبار موجود است`;
    } else {
        message = "ناموجود";
    };
    document.getElementById("in-stock").innerHTML = `<span>موجودی</span> : ${message}`;
};

function setProductPrice(price, finalPrice) {
    var message;
    if (price != finalPrice) {
        message = `<h2>${separate(finalPrice)} تومان</h2>
        <h4 style="text-decoration: line-through;color:#ddddcc">${separate(price)} تومان</h4>`;
    } else {
        message = `<h2>${separate(price)} تومان</h2>`;
    }
    document.getElementById("product-price-area").innerHTML = message
};

function changeProductColor(colorId, colorName, productStock,
    productPrice, productFinalPrice,
    cartItemQuantity, addProductToCartFunc) {
    var colors = document.getElementsByClassName('color-icon-area')[0].getElementsByTagName('a');
    for (var i = 0; i < colors.length; i++) {
        colors[i].style.borderColor = "gainsboro"
    };
    document.getElementById(colorId).style.borderColor = "blue";
    document.getElementById("color-name").innerText = "رنگ: " + colorName;
    setStockMessage(productStock);
    setProductPrice(productPrice, productFinalPrice);
    document.getElementById("sst").value = cartItemQuantity;
    document.getElementById("increaseProductQuantityButton").setAttribute("onclick", `increaseProductQuantity('sst', ${productStock})`);
    document.getElementById("addToCartButton").setAttribute("onclick", addProductToCartFunc);
};

function loginRequiredAlert(loginUrl) {
    Swal.fire({
        title: "برای این کار ابتدا می بایست وارد شوید",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "ورود",
        cancelButtonText: "نه ممنون",
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.assign(loginUrl);
        };
    });
};

function logoutAlert(logoutUrl) {
    Swal.fire({
        title: "مطمئنی؟",
        icon: "warning",
        showCancelButton: true,
        focusCancel: true,
        confirmButtonText: "خروج",
        cancelButtonText: "متوقف کردن",
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.assign(logoutUrl);
        };
    });
};

function showAlert(message, icon, position, onload) {
    function show() {
        var res = Swal.fire({
            position: position,
            icon: icon,
            title: message,
            showConfirmButton: false,
            timer: 1500
        });
        return res
    };
    if (onload === true) {
        window.onload = function () {
            return show()
        };
    };
    return show()
};

async function addProductToCartAlert(colors, baseProductId) {
    if (Object.keys(colors).length == 0) {
        showAlert("این محصول در حال حاضر موجود نمی‌باشد", "error", "center");
        return false
    };
    const inputOptions = new Promise((resolve) => {
        setTimeout(() => {
            resolve(colors);
        }, 1000);
    });
    const { value: productId } = await Swal.fire({
        title: "رنگ محصول را انتخاب کنید",
        input: "radio",
        confirmButtonText: "تایید",
        inputOptions,
        inputValidator: (value) => {
            if (!value) {
                return "باید یک رنگ را انتخاب کنید";
            };
        }
    });
    if (productId) {
        addProductToCart(productId, baseProductId);
    };
};

function addProductToCart(productId, baseProductId) {
    quantity = $("#sst").val()
    $.get("/cart/add-product-to-cart", {
        id: productId,
        base_product_id: baseProductId,
        quantity: quantity
    }).then(res => {
        showAlert(res["text"], res["icon"], res["position"]);
        $("#product-colors-area").html(res["product_colors_area"]);
        var a = document.getElementsByClassName('color-icon-area')[0].getElementsByTagName('a');
        a[0].style.borderColor = "gainsboro";
        $("#color-icon-" + productId).css("borderColor", "blue");
    });
};

function removeProductFromCart(itemId) {
    $.get("/cart/remove-product-from-cart", {
        item_id: itemId
    }).then(res => {
        if (res["icon"] == "success") {
            $(`#cart-item-area-${itemId}`).remove()
        };
        showAlert(res["text"], res["icon"], res["position"]);
        $("#cart-total-discounted-price").html(separate(res["cart_total_discounted_price"]))
        $("#cart-total-discounted").html(separate(res["cart_total_discounted"]))
        $("#cart-total-price").html(separate(res["cart_total_price"]))
    });
};

function changeCartItemQuantity(productId, baseProductId, itemId, quantity) {
    $.get("/cart/add-product-to-cart", {
        id: productId,
        base_product_id: baseProductId,
        quantity: quantity
    }).then(res => {
        if (res["icon"] == "error") {
            showAlert(res["text"], res["icon"], res["position"]);
        } else {
            $(`#cart-item-total-price-${itemId}`).html(separate(res["cart_item_total_price"]))
            $("#cart-total-discounted-price").html(separate(res["cart_total_discounted_price"]))
            $("#cart-total-discounted").html(separate(res["cart_total_discounted"]))
            $("#cart-total-price").html(separate(res["cart_total_price"]))
        };
    });
};

function increaseProductQuantity(inputId, maxVal) {
    var result = document.getElementById(inputId);
    var sst = result.value;
    if (!isNaN(sst) && sst < maxVal) {
        result.value++;
    };
};

function likeProduct(productId) {
    $.get("/products/like-product", {
        id: productId
    }).then(res => {
        if (res["like"]) {
            $(`#product-like-icon-${productId}`).html(`
                <span class="lnr">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15.5" height="15.5" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16" style="vertical-align: 0;">
                        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                    </svg>
                </span>
            `)
        } else if (res["dislike"]) {
            $(`#product-like-icon-${productId}`).html('<span class="lnr lnr-heart"></span>')
        } else {
            showAlert("خطایی رخ داد", "error", "top-end")
        };
    });
};

function createList() {
    var title = $("#list_title").val();
    var description = $("#list_description").val();
    var csrftoken = getCookie("csrftoken");
    $.post("/user/lists/create-list/", {
        csrfmiddlewaretoken: csrftoken,
        title: title,
        description: description
    }).then(res => {
        if (res["form"]) {
            $("#list-creation-form-area").html(`${res["form"]}`);
        } else {
            $("#list-creation-form").modal("hide");
            $("#user-lists").html(res["user_lists"])
            var emptyForm = `
                <div class="form-group text-right">
                    <label for="list_title">عنوان:</label>
                    <br/>
                    <input class="form-control"
                        type="text" name="title" id="list_title"
                        maxlength="${$("#list_title")[0].maxLenght}" required >
                </div>
                <div class="form-group text-right">
                    <label for="list_description">
                        توضیحات:  (اختیاری)
                    </label>
                    <br/>
                    <textarea name="description" class="form-control" rows="4" id="list_description"></textarea>
                </div>
            `
            $("#list-creation-form-area").html(emptyForm);
            showAlert("لیست شما با موفقیت ایجاد شد", "success", "center");
        };
    });
};

function editList(listId) {
    var title = $("#list_title").val();
    var description = $("#list_description").val();
    $.get("/user/lists/edit-list", {
        id: listId,
        title: title,
        description: description
    }).then(res => {
        if (res["form"]) {
            $("#edit-list-form-area").html(`${res["form"]}`);
        } else {
            var newListUrl = `/user/lists/${title}/`;
            var listDescription = description
            if (!description) {
                listDescription = `
                    <div class="text-muted">
                        هنوز توضیحاتی برای این لیست نوشته نشده است.
                    </div>
                `
            };
            $("#edit-list-form").modal("hide");
            $("#page-title").html(title);
            $("#page-url").html(title);
            $("#page-url")[0].href = newListUrl;
            $("#list-description").html(listDescription);
            window.history.pushState("", "", newListUrl);
            showAlert("لیست شما با موفقیت ویرایش شد", "success", "center");
        };
    });
};

function removeList(listId) {
    $.get("/user/lists/remove-list/", {
        id: listId
    }).then(res => {
        if (res["icon"] == "success") {
            $(`#list-area-${listId}`).remove();
        };
        showAlert(res["text"], res["icon"], res["position"]);
    });
};
