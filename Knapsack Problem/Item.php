<?php

class Item
{
    public string $name;
    public int $weight;
    public int $value;
    public float $sortKey;

    public function __construct(int $id, string $weight, string $value)
    {
        $this->name = "Item {$id}";
        $this->weight = (int) $weight;
        $this->value = (int) $value;
        $this->sortKey = $value / $weight;
    }
}