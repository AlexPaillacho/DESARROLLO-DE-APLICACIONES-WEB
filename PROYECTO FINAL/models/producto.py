class Producto:
    def __init__(self, sku, nombre, categoria, stock, tamano=None, peso=None):
        self.sku = sku
        self.nombre = nombre
        self.categoria = categoria
        self.stock = stock
        self.tamano = tamano
        self.peso = peso

    
    def __repr__(self):
        return f"<Producto {self.nombre} (SKU: {self.sku})>"