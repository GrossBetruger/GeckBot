use std::collections::HashMap;


async fn get_price(name: &str) {
    let resp = reqwest::get(
        format!("https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd", name))
        .await.unwrap();

    let parsed = resp
        .json::<HashMap<String, HashMap<String, f64>>>()
        .await.unwrap();
    println!("{:?}", parsed);
}

async fn get_all_coins() -> Vec<String>{
    let resp = reqwest::get("https://api.coingecko.com/api/v3/coins/list")
        .await.unwrap();

    let parsed = resp
        .json::<Vec<HashMap<String, String>>>()
        .await.unwrap();

    let names: Vec<String > = parsed.iter().map(|x| String::from(&x["name"])).collect();
    names
}


fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let coins = rt.block_on(get_all_coins());
    rt.block_on(get_price(&coins[0]));
}
