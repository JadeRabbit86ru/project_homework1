class CategoryIterator:
    def __init__(self, category):
        self.category = category
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        products = self.category.products
        if self.index < len(products):
            product = products[self.index]
            self.index += 1
            return product
        raise StopIteration
