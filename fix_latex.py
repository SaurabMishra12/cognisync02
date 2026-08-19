import re

file_path = r'C:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\evaluation\results\Paper\latex 7march.tex'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 40,000+ -> 35,000+
content = content.replace('40,000+', '35,000+')

# 2. Adaptive Routing Formula (Section 4.4)
old_eq = r'''\begin{equation}
  \mathrm{score}(d) =
    \frac{\alpha}{k+r_{\mathrm{dense}}(d)}+
    \frac{(1-\alpha)}{k+r_{\mathrm{lex}}(d)},
    \quad k=60,
\end{equation}
where $\alpha \in (0,1)$ is set adaptively by the query-type detector.
The detector classifies each query as semantic or exact-match based on
high-entropy token patterns: UUIDs, hexadecimal strings, versioned
endpoint paths, and uppercase alphanumeric error codes (see
Appendix~\ref{app:routing_spec} for the full deterministic specification).

\textbf{Adaptive weighting.} For semantic queries the detector sets
$\alpha = 0.5$ (equal-weight fusion). For exact-match queries it sets
$\alpha = 0.25$, up-weighting the lexical component while retaining a
non-zero dense contribution. This differs critically from the pre-fix
behavior, in which exact-match queries set $\alpha = 0$ (lexical-only),'''

new_eq = r'''\begin{equation}
  \mathrm{score}(d) =
    \frac{W_{\mathrm{dense}}}{k+r_{\mathrm{dense}}(d)}+
    \frac{W_{\mathrm{lexical}}}{k+r_{\mathrm{lex}}(d)},
    \quad k=60,
\end{equation}
where weights {\mathrm{dense}}$ and {\mathrm{lexical}}$ are set adaptively by the query-type detector.
The detector classifies each query as semantic or exact-match based on
high-entropy token patterns: UUIDs, hexadecimal strings, versioned
endpoint paths, and uppercase alphanumeric error codes (see
Appendix~\ref{app:routing_spec} for the full deterministic specification).

\textbf{Adaptive weighting.} For semantic queries the detector sets
{\mathrm{dense}} = 1.0$ and {\mathrm{lexical}} = 1.0$ (equal-weight fusion). For exact-match queries it sets
{\mathrm{dense}} = 0.2$ and {\mathrm{lexical}} = 3.0$, heavily up-weighting the lexical component while retaining a
non-zero dense contribution. This differs critically from the pre-fix
behavior, in which exact-match queries set {\mathrm{dense}} = 0.0$ and {\mathrm{lexical}} = 1.0$ (lexical-only),'''
content = content.replace(old_eq, new_eq)

old_app_b = r'''Upon exact-match classification, the routing sets the lexical weight
parameter $\alpha = 0.25$ in the RRF fusion equation, up-weighting the
lexical signal while retaining a non-zero dense contribution. Upon semantic
classification, $\alpha = 0.5$ (equal-weight). The pre-fix behavior set
$\alpha = 0$ for exact-match queries, which is equivalent to lexical-only'''
new_app_b = r'''Upon exact-match classification, the routing sets the weight
parameters {\mathrm{dense}} = 0.2$ and {\mathrm{lexical}} = 3.0$ in the RRF fusion equation, up-weighting the
lexical signal while retaining a non-zero dense contribution. Upon semantic
classification, {\mathrm{dense}} = 1.0$ and {\mathrm{lexical}} = 1.0$ (equal-weight). The pre-fix behavior set
{\mathrm{dense}} = 0.0$ and {\mathrm{lexical}} = 1.0$ for exact-match queries, which is equivalent to lexical-only'''
content = content.replace(old_app_b, new_app_b)

content = content.replace(r'($\alpha = 0.25$ for exact-match, $\alpha = 0.5$ for semantic) outperforms', r'({\mathrm{dense}}=0.2, W_{\mathrm{lexical}}=3.0$ for exact-match, {\mathrm{dense}}=1.0, W_{\mathrm{lexical}}=1.0$ for semantic) outperforms')

old_table6 = r'''Hybrid-Naive                   & 0.823 & 0.889 & 0.944 & 0.962 &
  Always-on RRF ($\alpha=0.5$) \\
CogniSync \textit{(pre-fix)}   & 0.823 & 0.861 & 0.944 & 0.934 &
  Semantic $\to$ RRF; exact-match $\to$ lexical-only ($\alpha=0$, \textbf{bug}) \\
CogniSync \textit{(post-fix)}  & 0.823 & 0.927 & 0.944 & 0.978 &
  Semantic $\to$ RRF ($\alpha=0.5$); exact-match $\to$ adaptive hybrid ($\alpha=0.25$) \\'''
new_table6 = r'''Hybrid-Naive                   & 0.823 & 0.889 & 0.944 & 0.962 &
  Always-on RRF ({\mathrm{d}}{=}1.0, W_{\mathrm{l}}{=}1.0$) \\
CogniSync \textit{(pre-fix)}   & 0.823 & 0.861 & 0.944 & 0.934 &
  Semantic $\to$ RRF; exact-match $\to$ lexical-only ({\mathrm{d}}{=}0$, \textbf{bug}) \\
CogniSync \textit{(post-fix)}  & 0.823 & 0.927 & 0.944 & 0.978 &
  Semantic $\to$ RRF ({\mathrm{d}}{=}1.0$); exact-match $\to$ adaptive hybrid ({\mathrm{l}}{=}3.0$) \\'''
content = content.replace(old_table6, new_table6)

old_sec7 = r'''on exact-match queries: the detector was setting $\alpha = 0$, discarding
the dense signal entirely and producing output identical to pure BM25
for 31.7\% of all queries. A 408-query benchmark would not have made
this equality exact; 35,000+ queries did.

\textbf{Implementing the fix.} We corrected the miscalibration by changing
the exact-match routing from $\alpha = 0$ (lexical-only) to $\alpha = 0.25$
(lexical-upweighted hybrid). This retains a non-zero dense contribution
for fallback robustness while still prioritizing lexical matching on
high-entropy tokens. The change required modifying a single parameter in
the query-type detector; the rest of the architecture is unchanged.

\textbf{Effect of the correction.} The improvement is concentrated on
the exact-match stratum, as expected. Exact-match MRR improved from 0.861
to 0.927, surpassing Hybrid-Naive's 0.889. The gain over Hybrid-Naive
confirms that $\alpha = 0.25$ (lexical-upweighted) outperforms $\alpha = 0.5$
(equal-weight) on this query type: when the query contains a UUID or error
code, the lexical signal deserves more weight, but discarding the dense'''
new_sec7 = r'''on exact-match queries: the detector was setting {\mathrm{dense}} = 0.0$, discarding
the dense signal entirely and producing output identical to pure BM25
for 31.7\% of all queries. A 408-query benchmark would not have made
this equality exact; 35,000+ queries did.

\textbf{Implementing the fix.} We corrected the miscalibration by changing
the exact-match routing from {\mathrm{dense}} = 0.0$ (lexical-only) to {\mathrm{dense}} = 0.2, W_{\mathrm{lexical}} = 3.0$
(lexical-upweighted hybrid). This retains a non-zero dense contribution
for fallback robustness while still prioritizing lexical matching on
high-entropy tokens. The change required modifying a single parameter in
the query-type detector; the rest of the architecture is unchanged.

\textbf{Effect of the correction.} The improvement is concentrated on
the exact-match stratum, as expected. Exact-match MRR improved from 0.861
to 0.927, surpassing Hybrid-Naive's 0.889. The gain over Hybrid-Naive
confirms that {\mathrm{dense}} = 0.2, W_{\mathrm{lexical}} = 3.0$ (lexical-upweighted) outperforms {\mathrm{dense}} = 1.0, W_{\mathrm{lexical}} = 1.0$
(equal-weight) on this query type: when the query contains a UUID or error
code, the lexical signal deserves more weight, but discarding the dense'''
content = content.replace(old_sec7, new_sec7)

content = content.replace(r'queries, adaptive hybrid ($\alpha=0.25$) achieves Recall@5 = 0.834 versus', r'queries, adaptive hybrid ({\mathrm{lexical}}{=}3.0$) achieves Recall@5 = 0.834 versus')
content = content.replace(r'fusion with query-dependent weighting ($\alpha = 0.25$ for exact-match)', r'fusion with query-dependent weighting ({\mathrm{dense}} = 0.2, W_{\mathrm{lexical}} = 3.0$ for exact-match)')

# 3. MS-MARCO 12% -> 18.1%
content = content.replace('compared to 12% on MS-MARCO', 'compared to 18.1% on MS-MARCO')
content = content.replace('under the validation layer versus 12%\n', 'under the validation layer versus 18.1%\n')

# 4. Cohen's d
old_tab5 = r'''CogniSync    & 0.526 & 0.981 & 0.982 & 0.996 & 0.883 & 0.874 & 0.856 & $-.052 \\
Hybrid-Naive & 0.499 & 0.971 & 0.972 & 0.995 & 0.873 & 0.862 & 0.844 & $-.094 \\'''
new_tab5 = r'''CogniSync    & 0.526 & 0.981 & 0.982 & 0.996 & 0.883 & 0.874 & 0.856 & $\phantom{-}.151 \\
Hybrid-Naive & 0.499 & 0.971 & 0.972 & 0.995 & 0.873 & 0.862 & 0.844 & $-.117 \\'''
content = content.replace(old_tab5, new_tab5)

old_app_c = r'''Effect-size interpretation:  \approx 0.052$ (Dense vs.~CogniSync, very
small);  \approx 0.094$ (Hybrid-Naive vs.~CogniSync, small);'''
new_app_c = r'''Effect-size interpretation:  \approx 0.151$ (Vanilla RAG vs.~CogniSync, small);  \approx -0.117$ (Hybrid-Naive vs.~CogniSync, small);'''
content = content.replace(old_app_c, new_app_c)

# 5. Latency 7.8x -> 8.0x
content = content.replace('.8\\times$ faster than', '.0\\times$ faster than')
content = content.replace('.8\\times$ the latency', '.0\\times$ the latency')

# 6. Wilcoxon p-values
old_tab4 = r'''CogniSync         & 0.792 & 0.898 & 0.955 & 0.856 & 0.882 &  < 10^{-40}$ & $-.011 \\
Hybrid-Naive      & 0.774 & 0.889 & 0.951 & 0.844 & 0.872 &  < 10^{-90}$ & $-.023 \\
Lexical (BM25)    & 0.726 & 0.838 & 0.912 & 0.796 & 0.826 &  < 10^{-300}$ & $-.071 \\'''
new_tab4 = r'''CogniSync         & 0.792 & 0.898 & 0.955 & 0.856 & 0.882 &  = 1.50\times 10^{-172}$ & $-.011 \\
Hybrid-Naive      & 0.774 & 0.889 & 0.951 & 0.844 & 0.872 &  = 1.61\times 10^{-112}$ & $-.023 \\
Lexical (BM25)    & 0.726 & 0.838 & 0.912 & 0.796 & 0.826 &  < 10^{-300}$ & $-.071 \\'''
content = content.replace(old_tab4, new_tab4)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Modifications applied successfully.")
