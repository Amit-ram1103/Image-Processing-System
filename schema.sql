CREATE TABLE Requests (
    request_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    status VARCHAR(20) NOT NULL,
    timestamp DATETIME DEFAULT GETDATE()
);

CREATE TABLE Products (
    product_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    request_id UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Requests(request_id),
    product_name VARCHAR(255) NOT NULL
);

CREATE TABLE Images (
    image_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    product_id UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Products(product_id),
    input_image_url TEXT NOT NULL,
    output_image_url TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'Processing'
);
