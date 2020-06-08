<?php

require_once('Item.php');
require_once('Knapsack.php');

$file = fopen('data.csv', 'r');
if (!$file) {
    echo "[Error] File doesn't exists.";
    exit(1);
}

$items = [];
$i = 0;
while (($data = fgetcsv($file)) !== false) {
    $items[] = new Item(++$i, ...$data);
}
fclose($file);

print("**** Add using Value strategy (Most Valuable First)...\n");
usort($items, fn(Item $a, Item $b) => $b->value <=> $a->value);
(new Knapsack(100))->run($items, 'value');

print("\n\n**** Add using Weight strategy (Less Weight First)...\n");
usort($items, fn(Item $a, Item $b) => $a->weight <=> $b->weight);
(new Knapsack(100))->run($items, 'weight');

print("\n\n**** Add using Value/Weight strategy...\n");
usort($items, fn(Item $a, Item $b) => $b->sortKey <=> $a->sortKey);
(new Knapsack(100))->run($items, 'sortKey', 'Value/Weight');