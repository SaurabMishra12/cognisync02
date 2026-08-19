# CTMC (Continuous-Time Markov Chain) — Exam Notes

---

## 1. Core Idea

- DTMC: changes at discrete steps $n = 1,2,3$
    
- CTMC: changes at continuous time $t \ge 0$
    
- Satisfies **Markov Property (memoryless)**
    

---

## 2. Markov Property (Definition)

$$  
P(X_{t_n}=j \mid X_{t_1}, \dots, X_{t_{n-1}})  
= P(X_{t_n}=j \mid X_{t_{n-1}})  
$$

**Meaning:** Future depends only on present, not past

---

## 3. Transition Probability

$$  
p_{ij}(t) = P(X_{t+s}=j \mid X_s=i)  
$$

- If homogeneous → depends only on $t$
    
- Independent of starting time $s$
    

---

## 4. Initial Condition

$$  
p_{ij}(0) = \delta_{ij}  
$$

- $\delta_{ij} = 1$ if $i=j$, else $0$
    

$$  
P(0) = I  
$$

---

## 5. Chapman–Kolmogorov Equation

$$  
p_{ij}(s+t) = \sum_{k \in S} p_{ik}(s), p_{kj}(t)  
$$

Matrix form:

$$  
P(s+t) = P(s)P(t)  
$$

---

## 6. Transition Rates (Generator Matrix $Q$)

### (a) Off-diagonal ($i \ne j$)

$$  
q_{ij} = \lim_{t \to 0^+} \frac{p_{ij}(t)}{t}  
$$

- Instantaneous transition rate from $i \to j$
    
- $q_{ij} \ge 0$
    

---

### (b) Diagonal

$$  
q_{ii} = \lim_{t \to 0^+} \frac{p_{ii}(t) - 1}{t}  
$$

- Rate of leaving state $i$
    
- $q_{ii} \le 0$
    

---

### (c) Key Property

$$  
q_{ii} = - \sum_{j \ne i} q_{ij}  
$$

- Row sum of $Q = 0$
    

---

## 7. Intuition

- System stays in a state for random time → then jumps
    

---

## 8. DTMC vs CTMC

|Feature|DTMC|CTMC|
|---|---|---|
|Time|Discrete $n$|Continuous $t$|
|Transition|Step-wise|Anytime|
|Parameter|$P$|$P(t), Q$|

---

## 9. Important Example

- Poisson Process:
    
    - States: $0,1,2,\dots$
        
    - Jumps: +1
        
    - Random arrival times
        

---

## 10. Small-Time Approximation

$$  
p_{ij}(dt) \approx q_{ij} \cdot dt \quad (i \ne j)  
$$

---

## 11. Generator Matrix $Q$

- Off-diagonal → positive
    
- Diagonal → negative
    
- Row sum = 0
    

---

# Ultra-Short Revision

- CTMC → continuous time
    
- $p_{ij}(t)$ → transition probability
    
- $P(0) = I$
    
- $P(s+t) = P(s)P(t)$
    
- $q_{ij} = \frac{dp_{ij}}{dt}\big|_{t=0}$
    
- $q_{ii} = -\sum_{j\ne i} q_{ij}$
    

---

# Quick Practice

**Q1:** State Chapman–Kolmogorov  
**Ans:** $P(s+t)=P(s)P(t)$

**Q2:** Why $q_{ii} < 0$?  
**Ans:** Probability flows out of state $i$

**Q3:** What is $P(0)$?  
**Ans:** Identity matrix

**Q4:** Meaning of $q_{ij}$?  
**Ans:** Instantaneous transition rate

---


# Infinitesimal Generator Matrix (Q) & Kolmogorov Equations — Exam Notes

---

## 1. Core Idea

- DTMC uses **probability matrix (P)**
    
- CTMC uses **rate matrix (Q)**
    

👉 (Q) tells:

- How fast we leave a state
    
- Where we go next (rates)
    

---

## 2. Generator Matrix (Q) Properties

### (a) Diagonal

$$  
q_{ii} \le 0  
$$

- Rate of leaving state (i)
    

---

### (b) Off-diagonal

$$  
q_{ij} \ge 0 \quad (i \ne j)  
$$

- Rate of transition (i \to j)
    

---

### (c) Row Sum Property

$$  
\sum_{j} q_{ij} = 0  
$$

👉 Equivalent:  
$$  
q_{ii} = - \sum_{j \ne i} q_{ij}  
$$

---

## 3. Types of States

- **Absorbing:**  
    $$  
    q_{ii} = 0  
    $$  
    → never leaves
    
- **Instantaneous:**  
    $$  
    q_{ii} = -\infty  
    $$  
    → leaves immediately
    
- **Stable/Regular:**  
    $$  
    0 < -q_{ii} < \infty  
    $$  
    → normal waiting time
    

---

## 4. Embedded Markov Chain

Convert (Q \to P):

$$  
p_{ij} = \frac{q_{ij}}{-q_{ii}} \quad (i \ne j)  
$$

$$  
p_{ii} = 0  
$$

👉 Interpretation:

- Ignore waiting time
    
- Only track jumps
    

---

## 5. Kolmogorov Equations

### Forward Equation

$$  
P'(t) = P(t)Q  
$$

---

### Backward Equation

$$  
P'(t) = QP(t)  
$$

---

### Initial Condition

$$  
P(0) = I  
$$

---

## 6. Solution of CTMC

$$  
P(t) = e^{Qt}  
$$

Where:  
$$  
e^{Qt} = I + Qt + \frac{Q^2 t^2}{2!} + \cdots  
$$

---

### Efficient Computation (Important)

If:  
$$  
Q = A D A^{-1}  
$$

Then:  
$$  
e^{Qt} = A e^{Dt} A^{-1}  
$$

---

## 7. Key Interpretation

- (Q) → rates
    
- (P(t)) → probabilities over time
    
- Differential equations describe evolution
    

---

## 8. Example (Embedded Chain)

Given:  
$$  
Q =  
\begin{pmatrix}  
-5 & 3 & 2 \  
1 & -2 & 1 \  
4 & 0 & -4  
\end{pmatrix}  
$$

Compute (P):

---

### Row 1:

$$  
p_{01} = \frac{3}{5}, \quad p_{02} = \frac{2}{5}  
$$

Row:  
$$  
(0, 3/5, 2/5)  
$$

---

### Row 2:

$$  
p_{10} = \frac{1}{2}, \quad p_{12} = \frac{1}{2}  
$$

Row:  
$$  
(1/2, 0, 1/2)  
$$

---

### Row 3:

$$  
p_{20} = 1, \quad p_{21} = 0  
$$

Row:  
$$  
(1, 0, 0)  
$$

---

### Final Matrix

$$  
P =  
\begin{pmatrix}  
0 & 3/5 & 2/5 \  
1/2 & 0 & 1/2 \  
1 & 0 & 0  
\end{pmatrix}  
$$

---

## 9. Ultra-Short Revision

- (q_{ii} \le 0), (q_{ij} \ge 0)
    
- Row sum = 0
    
- (p_{ij} = \frac{q_{ij}}{-q_{ii}})
    
- (P'(t) = P(t)Q), (QP(t))
    
- (P(t) = e^{Qt})
    

---

## 10. Quick Practice

**Q1:** Row sum property?  
**Ans:** $\sum_j q_{ij} = 0$

---

**Q2:** If $q_{kk} = 0$?  
**Ans:** Absorbing state

---

**Q3:** Forward equation?  
**Ans:** $P'(t) = P(t)Q$

---

**Q4:** Why use diagonalization?  
**Ans:** Simplifies computation of $e^{Qt}$

---

## 11. Key Intuition (1 line)

- (Q) controls **speed**, (P(t)) gives **probability evolution**
    

---# Stationary Distribution (CTMC) — Exam Notes

---

## 1. Core Idea

- CTMC reaches **long-run equilibrium** → stationary distribution ( \pi )
    
- Probabilities **do not change with time**
    

---

## 2. Two Definitions

### (a) Using Transition Matrix

$$  
\pi = \pi P(t), \quad \forall t \ge 0  
$$

👉 Hard to use since ( P(t) = e^{Qt} )

---

### (b) Using Generator Matrix (IMPORTANT)

$$  
\pi Q = 0  
$$

👉 This is the **main exam formula**

---

## 3. Conditions for Stationary Distribution

$$  
\pi Q = 0  
$$

$$  
\sum_i \pi_i = 1, \quad \pi_i \ge 0  
$$

---

## 4. Interpretation (Very Important)

- Flow **into state = flow out of state**
    
- No change → equilibrium
    

---

## 5. Steps to Solve Problems

1. Given ( Q )
    
2. Solve:  
    $$  
    \pi Q = 0  
    $$
    
3. Add:  
    $$  
    \sum \pi_i = 1  
    $$
    
4. Solve linear equations
    

---

## 6. Link with Kolmogorov Equation

From:  
$$  
P'(t) = P(t)Q  
$$

At stationarity:  
$$  
P'(t) = 0  
$$

So:  
$$  
\pi Q = 0  
$$

---

## 7. Embedded Markov Chain

- Derived from ( Q )
    
- Ignores waiting time
    
- Used for existence of stationary distribution
    

---

## 8. Important 2-State Result (VERY IMPORTANT)

Given:  
$$  
Q =  
\begin{pmatrix}  
-\mu & \mu \  
\lambda & -\lambda  
\end{pmatrix}  
$$

Solve:  
$$  
\pi Q = 0  
$$

---

### Balance Equation

$$  
\pi_0 \mu = \pi_1 \lambda  
$$

---

### Using Normalization

$$  
\pi_0 + \pi_1 = 1  
$$

---

### Final Answer

$$  
\pi_0 = \frac{\lambda}{\lambda + \mu}, \quad  
\pi_1 = \frac{\mu}{\lambda + \mu}  
$$

---

## 9. Example (Machine Model)

Given:

- ( q_{01} = 2 )
    
- ( q_{10} = 8 )
    

---

### Step 1: Build ( Q )

$$  
Q =  
\begin{pmatrix}  
-2 & 2 \  
8 & -8  
\end{pmatrix}  
$$

---

### Step 2: Solve

$$  
-2\pi_0 + 8\pi_1 = 0  
$$

$$  
\pi_0 = 4\pi_1  
$$

---

### Step 3: Normalize

$$  
\pi_0 + \pi_1 = 1  
$$

$$  
4\pi_1 + \pi_1 = 1  
$$

$$  
\pi_1 = \frac{1}{5}, \quad \pi_0 = \frac{4}{5}  
$$

---

### Final Result

- Working probability = ( 0.8 )
    
- Broken probability = ( 0.2 )
    

---

## 10. Ultra-Short Revision

- Stationary: no change in time
    
- ( \pi Q = 0 )
    
- ( \sum \pi_i = 1 )
    
- Balance: in-flow = out-flow
    

---

## 11. Quick Practice

**Q1:** Conditions for stationary distribution?  
**Ans:** ( \pi Q = 0 ), ( \sum \pi_i = 1 )

---

**Q2:** Why use ( \pi Q = 0 )?  
**Ans:** Rate of change = 0

---

**Q3:** Physical meaning?  
**Ans:** Flow balance

---

**Q4:** Long-run probability?  
**Ans:** Stationary distribution

---

## 12. Key Intuition (1 line)

- DTMC: ( \pi P = \pi )
    
- CTMC: ( \pi Q = 0 )
    

---# Counting Process — Exam Notes

---

## 1. Core Idea

- We model **number of events up to time (t)**
    
- Leads to a **Counting Process**
    

---

## 2. Definition

A counting process ( {N(t), t \ge 0} ) is a stochastic process such that:

---

### (a) Values

$$  
N(t) \in {0,1,2,\dots}  
$$

👉 Counts number of events

---

### (b) Non-Decreasing

$$  
N(t_2) \ge N(t_1) \quad \text{for } t_2 \ge t_1  
$$

👉 Events accumulate, never decrease

---

### (c) Initial Condition

$$  
N(0) = 0  
$$

👉 No events at time 0

---

## 3. Interpretation

$$  
N(t) = \text{Number of events that occurred up to time } t  
$$

---

## 4. Intuition (1 line)

- Process **counts arrivals over time**
    

---

## 5. Examples (Important)

- Customers arriving in a queue
    
- Phone calls at a call center
    
- Failures of a machine
    
- Radioactive decay events
    

---

## 6. Ultra-Short Revision

- ( N(t) ) → number of events
    
- Integer valued
    
- Non-decreasing
    
- ( N(0)=0 )
    

---

## 7. Quick Practice

**Q1:** Why is (N(t)) non-decreasing?  
**Ans:** Events accumulate, cannot decrease

---

**Q2:** What does (N(t)) represent?  
**Ans:** Number of events up to time (t)

---

**Q3:** Can (N(t)) be negative?  
**Ans:** No

---

## 8. Key Intuition (Exam Line)

- Counting process tracks **how many events happened till time (t)**
    

---