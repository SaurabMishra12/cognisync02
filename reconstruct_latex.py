import sys
import re

log_path = r'C:\Users\msaur\.gemini\antigravity\brain\9688cc06-d880-4c35-837e-ed20a3a61692\.system_generated\logs\overview.txt'
sys.stdout.reconfigure(encoding='utf-8')

with open(log_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find the diff block for the latex file
# In overview.txt, it looks like a JSON log entry with a "content" field
idx = text.rfind(r'\documentclass[sigconf,authordraft]{acmart}')
if idx == -1:
    print('Failed to find start.')
    sys.exit(1)

start_idx = text.rfind('"content":', 0, idx)
end_idx = text.find('"}', idx)

if start_idx == -1 or end_idx == -1:
    print('Failed to extract bounds.')
    sys.exit(1)

raw_content = text[start_idx:end_idx+2]
lines = raw_content.split('\\n')

extracted_lines = []
for line in lines:
    line = line.replace('\\"', '"').replace('\\\\', '\\')
    if line.startswith('+'):
        extracted_lines.append(line[1:])
    elif line.startswith(' '):
        extracted_lines.append(line[1:])

if not extracted_lines:
    print('Failed to parse lines.')
    sys.exit(1)

original_latex = '\n'.join(extracted_lines)

# Apply fixes

# 1. 40,000+ -> 35,000+
original_latex = original_latex.replace('40,000+', '35,000+')

# 2. Adaptive Routing Formula and text
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
where weights $W_{\mathrm{dense}}$ and $W_{\mathrm{lexical}}$ are set adaptively by the query-type detector.
The detector classifies each query as semantic or exact-match based on
high-entropy token patterns: UUIDs, hexadecimal strings, versioned
endpoint paths, and uppercase alphanumeric error codes (see
Appendix~\ref{app:routing_spec} for the full deterministic specification).

\textbf{Adaptive weighting.} For semantic queries the detector sets
$W_{\mathrm{dense}} = 1.0$ and $W_{\mathrm{lexical}} = 1.0$ (equal-weight fusion). For exact-match queries it sets
$W_{\mathrm{dense}} = 0.2$ and $W_{\mathrm{lexical}} = 3.0$, heavily up-weighting the lexical component while retaining a
non-zero dense contribution. This differs critically from the pre-fix
behavior, in which exact-match queries set $W_{\mathrm{dense}} = 0.0$ and $W_{\mathrm{lexical}} = 1.0$ (lexical-only),'''

if old_eq in original_latex:
    original_latex = original_latex.replace(old_eq, new_eq)
else:
    print('Warning: old_eq not found')

original_latex = original_latex.replace(
    r'''Upon exact-match classification, the routing sets the lexical weight
parameter $\alpha = 0.25$ in the RRF fusion equation, up-weighting the
lexical signal while retaining a non-zero dense contribution. Upon semantic
classification, $\alpha = 0.5$ (equal-weight). The pre-fix behavior set
$\alpha = 0$ for exact-match queries, which is equivalent to lexical-only''',
    r'''Upon exact-match classification, the routing sets the weight
parameters $W_{\mathrm{dense}} = 0.2$ and $W_{\mathrm{lexical}} = 3.0$ in the RRF fusion equation, up-weighting the
lexical signal while retaining a non-zero dense contribution. Upon semantic
classification, $W_{\mathrm{dense}} = 1.0$ and $W_{\mathrm{lexical}} = 1.0$ (equal-weight). The pre-fix behavior set
$W_{\mathrm{dense}} = 0.0$ and $W_{\mathrm{lexical}} = 1.0$ for exact-match queries, which is equivalent to lexical-only'''
)

original_latex = original_latex.replace(
    r'($\alpha = 0.25$ for exact-match, $\alpha = 0.5$ for semantic) outperforms',
    r'($W_{\mathrm{dense}}=0.2, W_{\mathrm{lexical}}=3.0$ for exact-match, $W_{\mathrm{dense}}=1.0, W_{\mathrm{lexical}}=1.0$ for semantic) outperforms'
)

original_latex = original_latex.replace(
    r'''Hybrid-Naive                   & 0.823 & 0.889 & 0.944 & 0.962 &
  Always-on RRF ($\alpha=0.5$) \\
CogniSync \textit{(pre-fix)}   & 0.823 & 0.861 & 0.944 & 0.934 &
  Semantic $\to$ RRF; exact-match $\to$ lexical-only ($\alpha=0$, \textbf{bug}) \\
CogniSync \textit{(post-fix)}  & 0.823 & 0.927 & 0.944 & 0.978 &
  Semantic $\to$ RRF ($\alpha=0.5$); exact-match $\to$ adaptive hybrid ($\alpha=0.25$) \\''',
    r'''Hybrid-Naive                   & 0.823 & 0.889 & 0.944 & 0.962 &
  Always-on RRF ($W_{\mathrm{d}}{=}1.0, W_{\mathrm{l}}{=}1.0$) \\
CogniSync \textit{(pre-fix)}   & 0.823 & 0.861 & 0.944 & 0.934 &
  Semantic $\to$ RRF; exact-match $\to$ lexical-only ($W_{\mathrm{d}}{=}0$, \textbf{bug}) \\
CogniSync \textit{(post-fix)}  & 0.823 & 0.927 & 0.944 & 0.978 &
  Semantic $\to$ RRF ($W_{\mathrm{d}}{=}1.0$); exact-match $\to$ adaptive hybrid ($W_{\mathrm{l}}{=}3.0$) \\'''
)

original_latex = original_latex.replace(
    r'''on exact-match queries: the detector was setting $\alpha = 0$, discarding
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
code, the lexical signal deserves more weight, but discarding the dense''',
    r'''on exact-match queries: the detector was setting $W_{\mathrm{dense}} = 0.0$, discarding
the dense signal entirely and producing output identical to pure BM25
for 31.7\% of all queries. A 408-query benchmark would not have made
this equality exact; 35,000+ queries did.

\textbf{Implementing the fix.} We corrected the miscalibration by changing
the exact-match routing from $W_{\mathrm{dense}} = 0.0$ (lexical-only) to $W_{\mathrm{dense}} = 0.2, W_{\mathrm{lexical}} = 3.0$
(lexical-upweighted hybrid). This retains a non-zero dense contribution
for fallback robustness while still prioritizing lexical matching on
high-entropy tokens. The change required modifying a single parameter in
the query-type detector; the rest of the architecture is unchanged.

\textbf{Effect of the correction.} The improvement is concentrated on
the exact-match stratum, as expected. Exact-match MRR improved from 0.861
to 0.927, surpassing Hybrid-Naive's 0.889. The gain over Hybrid-Naive
confirms that $W_{\mathrm{dense}} = 0.2, W_{\mathrm{lexical}} = 3.0$ (lexical-upweighted) outperforms $W_{\mathrm{dense}} = 1.0, W_{\mathrm{lexical}} = 1.0$
(equal-weight) on this query type: when the query contains a UUID or error
code, the lexical signal deserves more weight, but discarding the dense'''
)

original_latex = original_latex.replace(
    r'queries, adaptive hybrid ($\alpha=0.25$) achieves Recall@5 = 0.834 versus',
    r'queries, adaptive hybrid ($W_{\mathrm{lexical}}{=}3.0$) achieves Recall@5 = 0.834 versus'
)

original_latex = original_latex.replace(
    r'fusion with query-dependent weighting ($\alpha = 0.25$ for exact-match)',
    r'fusion with query-dependent weighting ($W_{\mathrm{dense}} = 0.2, W_{\mathrm{lexical}} = 3.0$ for exact-match)'
)

# 3. MS-MARCO 12% -> 18.1%
original_latex = original_latex.replace('compared to 12% on MS-MARCO', 'compared to 18.1% on MS-MARCO')
original_latex = original_latex.replace('under the validation layer versus 12%', 'under the validation layer versus 18.1%')

# 4. Cohen's d
original_latex = original_latex.replace(
    r'''CogniSync    & 0.526 & 0.981 & 0.982 & 0.996 & 0.883 & 0.874 & 0.856 & $-$0.052 \\
Hybrid-Naive & 0.499 & 0.971 & 0.972 & 0.995 & 0.873 & 0.862 & 0.844 & $-$0.094 \\''',
    r'''CogniSync    & 0.526 & 0.981 & 0.982 & 0.996 & 0.883 & 0.874 & 0.856 & $\phantom{-}$0.151 \\
Hybrid-Naive & 0.499 & 0.971 & 0.972 & 0.995 & 0.873 & 0.862 & 0.844 & $-$0.117 \\'''
)

original_latex = original_latex.replace(
    r'''Effect-size interpretation: $d \approx 0.052$ (Dense vs.~CogniSync, very
small); $d \approx 0.094$ (Hybrid-Naive vs.~CogniSync, small);''',
    r'''Effect-size interpretation: $d \approx 0.151$ (Vanilla RAG vs.~CogniSync, small); $d \approx -0.117$ (Hybrid-Naive vs.~CogniSync, small);'''
)

# 5. Latency 7.8x -> 8.0x
original_latex = original_latex.replace(r'7.8\times', r'8.0\times')

# 6. Wilcoxon p-values
original_latex = original_latex.replace(
    r'''CogniSync         & 0.792 & 0.898 & 0.955 & 0.856 & 0.882 & $p < 10^{-40}$ & $-$0.011 \\
Hybrid-Naive      & 0.774 & 0.889 & 0.951 & 0.844 & 0.872 & $p < 10^{-90}$ & $-$0.023 \\
Lexical (BM25)    & 0.726 & 0.838 & 0.912 & 0.796 & 0.826 & $p < 10^{-300}$ & $-$0.071 \\''',
    r'''CogniSync         & 0.792 & 0.898 & 0.955 & 0.856 & 0.882 & $p = 1.50\times 10^{-172}$ & $-$0.011 \\
Hybrid-Naive      & 0.774 & 0.889 & 0.951 & 0.844 & 0.872 & $p = 1.61\times 10^{-112}$ & $-$0.023 \\
Lexical (BM25)    & 0.726 & 0.838 & 0.912 & 0.796 & 0.826 & $p < 10^{-300}$ & $-$0.071 \\'''
)

target_path = r'C:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\evaluation\results\Paper\latex 7march.tex'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(original_latex)

print(f'Successfully wrote {len(original_latex)} characters to {target_path}')
