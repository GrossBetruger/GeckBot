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


fn main() {
    let mut rt = tokio::runtime::Runtime::new().unwrap();
    let future = get_price();
    rt.block_on(future);
}
