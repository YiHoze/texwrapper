If (!$args[1]) { $zoom = 1.75}
else { $zoom = $args[1] }
pdf2htmlex --zoom=$zoom --external-hint-tool=ttfautohint $args[0]