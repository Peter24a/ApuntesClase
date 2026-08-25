import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "01_documento.md"
OUTPUT = ROOT / "contenido" / "diagramas"


def escape_tex(value):
    value = value.replace("#quot;", '"').replace('\\"', '"')
    corrections = {
        "opcion": "opción", "numero": "número", "calificacion": "calificación",
        "anio": "año", "maximo": "máximo", "menu": "menú", "limite": "límite",
    }
    for original, corrected in corrections.items():
        value = re.sub(r"\b" + original + r"\b", corrected, value)
    parts = re.split(r"<br\s*/?>", value, flags=re.I)
    result = []
    replacements = [
        ("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
        ("$", r"\$"), ("#", r"\#"), ("_", r"\_"),
        ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for part in parts:
        for old, new in replacements:
            part = part.replace(old, new)
        result.append(part.strip())
    return r"\\".join(result)


def parse_node(token):
    token = token.strip()
    match = re.match(r"^([A-Za-z][A-Za-z0-9_]*)(.*)$", token, re.S)
    if not match:
        raise ValueError("Nodo no reconocido: " + token)
    ident, shape = match.groups()
    shape = shape.strip()
    if not shape:
        return ident, None, None
    quoted = re.findall(r'"(.*?)"', shape, re.S)
    label = quoted[-1] if quoted else shape.strip("[]{}()/\\ ")
    if shape.startswith("(["):
        style = "iniciofin"
    elif shape.startswith("{{"):
        style = "proceso"
    elif shape.startswith("{"):
        style = "decision"
    elif shape.startswith("[/"):
        style = "entradaSalida"
    elif shape.startswith("[\\"):
        style = "documento"
    else:
        style = "proceso"
    return ident, style, escape_tex(label)


def parse_edge(line):
    patterns = [
        (r"^(.*?)\s+-\.\s*(.*?)\s*\.->\s+(.*?)$", True),
        (r"^(.*?)\s+--\s*(.*?)\s*-->\s+(.*?)$", False),
        (r"^(.*?)\s+-->\s+(.*?)$", False),
    ]
    for pattern, dotted in patterns:
        match = re.match(pattern, line)
        if not match:
            continue
        groups = match.groups()
        if len(groups) == 2:
            return groups[0], "", groups[1], dotted
        return groups[0], groups[1], groups[2], dotted
    return None


def mermaid_blocks(markdown):
    fence = chr(96) * 3
    pattern = re.escape(fence) + r"mermaid\s*\n(.*?)\n" + re.escape(fence)
    return re.findall(pattern, markdown, flags=re.S)


def render_integrator(nodes):
    def item(ident):
        style, label = nodes[ident]
        return style, label

    placements = [
        ("A", "", ""),
        ("B", ",below=of a", ""),
        ("C", ",below=of b", ""),
        ("D", ",below=of c", ""),
        ("E", ",left=42mm of d", ""),
        ("F", ",below=of d", ""),
        ("G", ",below=of f", ""),
        ("H", ",below=of g", ""),
        ("I", ",below=of h", ""),
        ("J", ",right=42mm of h", ""),
        ("K", ",below=of i", ""),
        ("L", ",below=of k", ""),
        ("M", ",below=of l", ""),
        ("N", ",below=of m", ""),
        ("O", ",below=of n", ""),
        ("P", ",right=42mm of m", ""),
        ("Q", ",below=of p", ""),
    ]
    output = [
        r"\begin{center}",
        r"\begin{adjustbox}{max width=\textwidth,max totalheight=.72\textheight,keepaspectratio}",
        r"\begin{tikzpicture}[flujo,node distance=5mm and 14mm]",
    ]
    for ident, placement, _ in placements:
        style, label = item(ident)
        wrapping = ",text width=45mm" if len(label) > 36 or r"\\" in label else ""
        output.append(
            "  \\node[" + style + wrapping + placement + "] (" + ident.lower() + ") {" + label + "};"
        )
    output.extend([
        r"  \node[conector,left=52mm of c] (ca2) {A};",
        r"  \node[conector,left=52mm of k] (ca1) {A};",
        r"  \node[conector,right=52mm of f] (cc1) {C};",
        r"  \node[conector,right=52mm of k] (cc2) {C};",
        r"  \node[conector,left=52mm of m] (cb2) {B};",
        r"  \node[conector,left=52mm of o] (cb1) {B};",
        r"  \draw[draw=AzulLinea] (a) -- (b);",
        r"  \draw[draw=TurquesaLinea] (b) -- (c);",
        r"  \draw[draw=RosaLinea] (c) -- (d);",
        r"  \draw[draw=VerdeLinea] (d.west) -- node[etiqueta,above=2pt] {SÍ} (e.east);",
        r"  \draw[draw=MoradoLinea] (e.south) |- ($(i.south)!.25!(k.north)$);",
        r"  \draw[draw=NaranjaLinea] (d) -- node[etiqueta,right=2pt] {NO} (f);",
        r"  \draw[draw=VerdeLinea] (f) -- node[etiqueta,right=2pt] {SÍ} (g);",
        r"  \draw[draw=NaranjaLinea] (f.east) -- node[etiqueta,above=2pt] {NO} (cc1);",
        r"  \draw[draw=MoradoLinea] (cc2) |- ($(i.south)!.5!(k.north)$);",
        r"  \draw[draw=AzulLinea] (g) -- (h);",
        r"  \draw[draw=VerdeLinea] (h) -- node[etiqueta,right=2pt] {SÍ} (i);",
        r"  \draw[draw=NaranjaLinea] (h.east) -- node[etiqueta,above=2pt] {NO} (j.west);",
        r"  \draw[draw=TurquesaLinea] (i) -- (k);",
        r"  \draw[draw=MoradoLinea] (j.south) |- ($(i.south)!.75!(k.north)$);",
        r"  \draw[draw=VerdeLinea] (k.west) -- node[etiqueta,above=2pt] {SÍ} (ca1);",
        r"  \draw[draw=MoradoLinea] (ca2) |- ($(b.south)!.5!(c.north)$);",
        r"  \draw[draw=NaranjaLinea] (k) -- node[etiqueta,right=2pt] {NO} (l);",
        r"  \draw[draw=AzulLinea] (l) -- (m);",
        r"  \draw[draw=TurquesaLinea] (m) -- (n);",
        r"  \draw[draw=RosaLinea] (n) -- (o);",
        r"  \draw[draw=MoradoLinea] (o.west) -- (cb1);",
        r"  \draw[draw=MoradoLinea] (cb2) |- ($(l.south)!.5!(m.north)$);",
        r"  \draw[draw=MoradoLinea,dashed] (m.east) -- node[etiqueta,above=2pt] {Límite alcanzado} (p.west);",
        r"  \draw[draw=AzulLinea] (p) -- (q);",
        r"\end{tikzpicture}",
        r"\end{adjustbox}",
        r"\end{center}",
    ])
    return "\n".join(output) + "\n"


def render(block, number):
    nodes, order, edges = {}, [], []
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("graph "):
            continue
        parsed = parse_edge(line)
        if not parsed:
            continue
        source_token, label, target_token, dotted = parsed
        source, target = parse_node(source_token), parse_node(target_token)
        for ident, style, text in (source, target):
            if ident not in nodes:
                nodes[ident] = [style or "proceso", text or ident]
                order.append(ident)
            elif style:
                nodes[ident] = [style, text]
        edges.append((source[0], target[0], escape_tex(label), dotted))

    is_integrator = (
        set("ABCDEFGHIJKLMNOPQ").issubset(nodes)
        and any("saldo = 1000" in label for _, label in nodes.values())
        and any("FOR fase" in label for _, label in nodes.values())
    )
    if is_integrator:
        return render_integrator(nodes)

    index = {ident: position for position, ident in enumerate(order)}
    output = [
        r"\begin{center}",
        r"\begin{adjustbox}{max width=\textwidth,max totalheight=.72\textheight,keepaspectratio}",
        r"\begin{tikzpicture}[flujo,node distance=5mm and 14mm]",
    ]
    for position, ident in enumerate(order):
        style, label = nodes[ident]
        placement = "" if position == 0 else ",below=of n" + str(position - 1)
        wrapping = ",text width=45mm" if len(label) > 36 or r"\\" in label else ""
        output.append(
            r"  \node[" + style + placement + wrapping + "] (n" + str(position) + ") {" + label + "};"
        )

    forward_count, back_count = 0, 0
    palette = ["AzulLinea", "TurquesaLinea", "RosaLinea", "MoradoLinea"]
    for edge_number, (source, target, label, dotted) in enumerate(edges):
        start, finish = index[source], index[target]
        vertical_label = (
            r" node[etiqueta,right=2pt,pos=.45] {" + label + "}"
            if label else ""
        )
        horizontal_label = (
            r" node[etiqueta,above=2pt,pos=.45] {" + label + "}"
            if label else ""
        )
        normalized = label.upper()
        if "YES" in normalized or "SÍ" in normalized:
            color = "VerdeLinea"
        elif "NO" in normalized:
            color = "NaranjaLinea"
        elif dotted or finish < start:
            color = "MoradoLinea"
        else:
            color = palette[edge_number % len(palette)]
        options = ["draw=" + color]
        if dotted:
            options.append("dashed")
        option = "[" + ",".join(options) + "]"
        if finish == start + 1:
            output.append(
                r"  \draw" + option + " (n" + str(start) + ") --" +
                vertical_label + " (n" + str(finish) + ");"
            )
        elif finish > start:
            forward_count += 1
            distance = 38 + 5 * (forward_count % 3)
            output.append(
                r"  \draw" + option + " (n" + str(start) + ".east) -- " +
                horizontal_label + " ++(" + str(distance) + "mm,0) |- " +
                " (n" + str(finish) + ".east);"
            )
        else:
            back_count += 1
            distance = 38 + 5 * (back_count % 3)
            if finish > 0:
                merge = (
                    "($(n" + str(finish - 1) + ".south)!.5!(n" +
                    str(finish) + ".north)$)"
                )
            else:
                merge = "($(n0.north)+(0,3mm)$)"
            output.append(
                r"  \draw" + option + " (n" + str(start) + ".west) -- " +
                horizontal_label + " ++(-" + str(distance) + "mm,0) |- " +
                merge + ";"
            )
    output.extend([r"\end{tikzpicture}", r"\end{adjustbox}", r"\end{center}"])
    return "\n".join(output) + "\n"


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    blocks = mermaid_blocks(SOURCE.read_text(encoding="utf-8"))
    for previous in OUTPUT.glob("diagrama-*.tex"):
        previous.unlink()
    for number, block in enumerate(blocks, 1):
        destination = OUTPUT / ("diagrama-" + format(number, "02d") + ".tex")
        destination.write_text(render(block, number), encoding="utf-8")
    print("Generados", len(blocks), "diagramas TikZ.")


if __name__ == "__main__":
    main()
