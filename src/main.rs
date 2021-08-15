use reqwest::*;
use std::collections::HashMap;
use tokio::task;
use futures::prelude::*;
use tokio::*;


async fn get_price() {
    let resp = reqwest::get("https://api.coingecko.com/api/v3/simple/price?ids=cardano&vs_currencies=usd")
        .await.unwrap();

    let parsed = resp
        .json::<HashMap<String, HashMap<String, f64>>>()
        .await.unwrap();
    println!("{:?}", parsed);
}

async fn get_all_coins() {
    let resp = reqwest::get("https://api.coingecko.com/api/v3/coins/list")
        .await.unwrap();

    let parsed = resp
        .json::<Vec<HashMap<String, String>>>()
        .await.unwrap();
    println!("{:?}", parsed);
}


fn main() {
    let mut rt = tokio::runtime::Runtime::new().unwrap();
    let future = get_all_coins();
    rt.block_on(future);
}
