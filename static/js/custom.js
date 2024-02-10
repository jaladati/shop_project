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

function setProductFilter(data) {
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
    deleteParameterWithOutReload("paginate_change");

    $.get("/products/filter", paramData).then(res => {
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

function replyComment(parentId, userName) {
    document.getElementById("parentId").value = parentId;
    document.getElementById("myTab").scrollIntoView({ behavior: "smooth" });
    var comment = document.getElementById("commentText");
    comment.focus();
    comment.placeholder = `پاسخ برای نظر ${userName}`
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


function separate(number) {
    return (number).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};


function setProductPrice(price, finalPrice) {
    var message;
    if (price != finalPrice) {
        message = `<h2>\$${separate(finalPrice)}</h2>
        <h4 style="text-decoration: line-through;color:#ddddcc">\$${separate(price)}</h4>`;
    } else {
        message = `<h2>\$${separate(price)}</h2>`;
    }
    document.getElementById("product-price-area").innerHTML = message
};


function setProductColor(colorId, colorName, productStock, productPrice, productFinalPrice) {
    var a = document.getElementsByClassName('color-icon-area')[0].getElementsByTagName('a')
    for (var i = 0; i < a.length; i++) {
        a[i].style.borderColor = "gainsboro"
    }
    document.getElementById(colorId).style.borderColor = "blue";
    document.getElementById("color-name").innerText = "رنگ: " + colorName;
    setStockMessage(productStock);
    setProductPrice(productPrice, productFinalPrice);
};


function productInStockFilter() {
    var isChecked = document.getElementById("toggle-switch-checkbox").checked;
    if (isChecked) {
        setProductFilter({ "in_stock": "true" })
    } else {
        setProductFilter({ "in_stock": "false" })
    };
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


function showSuccessAlert(message) {
    window.onload = function () {
        Swal.fire({
            position: "top-end",
            icon: "success",
            title: message,
            showConfirmButton: false,
            timer: 1500
        });
    };
};
