module c17 (G1gat,G2gat,G3gat,G6gat,G7gat,G22gat,G23gat);

input G1gat,G2gat,G3gat,G6gat,G7gat;

output G22gat,G23gat;

wire G10gat,G11gat,G16gat,G19gat;

nand2 gate( .a(G1gat), .b(G3gat), .O(G10gat) );
nand2 gate( .a(G3gat), .b(G6gat), .O(G11gat) );
nand2 gate( .a(G2gat), .b(G11gat), .O(G16gat) );
nand2 gate( .a(G11gat), .b(G7gat), .O(G19gat) );
nand2 gate( .a(G10gat), .b(G16gat), .O(G22gat) );
nand2 gate( .a(G16gat), .b(G19gat), .O(G23gat) );

endmodule
