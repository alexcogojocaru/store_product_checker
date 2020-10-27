# store_product_checker

<h3>python app that checks if there are available products in a specific store</h3>
<h3><b>Description</b></h3>

<ul>
    <li>
        <p><b>seller</b> - the root tag for the product description</p>
    </li>
    <li>
        <p><b>seller_name</b> - the name of the store</p>
        <ul>
            <li><b>name</b> - name of the product</li>
            <li><b>link</b> - link to the page that needs a request</li>
        </ul>
        <h4>This part needs webscraping</h4>
        <ul>
            <li><b>div_name</b> - the div name that wraps the product info</li>
            <li><b>status</b> - the name of the class that describes the product's availability</li>
            <li><b>tag</b> - the tag that wraps the status (ex: p, div...)</li>
            <li><b>in_stock</b> - the keyword for the stock being available</li>
            <li><b>out_stock</b> - the keyword for the stock not being available</li>
        </ul>
    </li>
</ul>
