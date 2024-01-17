var inputUrl = new URL(window.location.href);
var inputParams = new URLSearchParams(inputUrl.search);

function updateInputUrlAndInputParams() {
    inputUrl = new URL(window.location.href);
    inputParams = new URLSearchParams(inputUrl.search);
}

function setParameter(name, value) {
    let inputUrl = new URL(window.location.href);
    let inputParams = new URLSearchParams(inputUrl.search);

    inputParams.set(name, value);
    window.location.assign(inputUrl.href.split("?")[0] + "?" + inputParams);
}

function deleteParameter(name) {
    let inputUrl = new URL(window.location.href);
    let inputParams = new URLSearchParams(inputUrl.search);

    inputParams.delete(name)
    window.location.assign(inputUrl.href.split("?")[0] + "?" + inputParams);
}

function setParameterWithOutReload(name, value) {
    updateInputUrlAndInputParams()
    inputParams.set(name, value)
    var url = inputUrl.href.split("?")[0] + "?" + inputParams
    window.history.pushState("", "", url);
}

function deleteParameterWithOutReload(name) {
    updateInputUrlAndInputParams()
    inputParams.delete(name)
    var url = inputUrl.href.split("?")[0] + "?" + inputParams
    window.history.pushState("", "", url);
}

function setProductFilter(data) {
    for (let key in data) {
        setParameterWithOutReload(key, data[key])
    };
    var paramData = {};
    updateInputUrlAndInputParams();

    for (let [key, value] of inputParams) {
        paramData[key] = value;
    };

    if ("paginate_change" in paramData){
        deleteParameterWithOutReload("page")
    }

    deleteParameterWithOutReload("category_change");
    deleteParameterWithOutReload("paginate_change");

    $.get("/products/filter", paramData).then(res => {
        if (res["categories"]) {
            $("#category-aria").html(res["categories"]);
        } else if (res["paginates"]) {
            $(".paginate").html(res["paginates"]);
        };
        $("#products-aria").html(res["products"]);
        $(".pagination").html(res["pagination"]);
        $("#common-filter").html(res["price_filter"])
    });
}

