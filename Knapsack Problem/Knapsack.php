<?php

class Knapsack
{
    public array $items = [];
    public float $totalCapacity;
    public float $capacityLeft;

    public function __construct(float $capacity)
    {
        $this->capacityLeft = $this->totalCapacity = $capacity;
    }

    public function addItem(Item $item): bool
    {
        if ($this->capacityLeft <= 0) {
            return false;
        }

        if (($this->capacityLeft - $item->weight) < 0) {
            return false;
        }

        $this->items[] = $item;
        $this->capacityLeft -= $item->weight;

        return true;
    }

    public function run(array $orderedItems, string $key, string $displayKey = null)
    {
        $displayKey ??= ucfirst($key);

        foreach ($orderedItems as $item) {
            if ($this->capacityLeft <= 0) {
                break;
            }
        
            $calculatedCapacityLeft = $this->capacityLeft - $item->weight;

            $keyValue = $item->$key;
            if (is_float($keyValue)) {
                $keyValue = number_format($keyValue, 4);
            }
        
            print("Adding {$item->name}\t({$displayKey}: {$keyValue})\t->\tCapacity: {$this->capacityLeft} - {$item->weight} = {$calculatedCapacityLeft}");
            print("\t" . ($this->addItem($item) ? '✔️' : '❌') . "\n");
        }
        print("**** Total Items Added: " . count($this->items) . "\n");
    }
}