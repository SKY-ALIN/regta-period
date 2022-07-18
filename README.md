# regta-period

**Library to make moment-independent periods in python.
It's designed specially for [Regta Framework](https://github.com/SKY-ALIN/regta), 
but with an ability to use it independently.**

[![versions](https://img.shields.io/pypi/pyversions/regta-period.svg)](https://github.com/SKY-ALIN/regta-period)
[![PyPI version](https://badge.fury.io/py/regta-period.svg)](https://pypi.org/project/regta-period/)
[![license](https://img.shields.io/github/license/SKY-ALIN/regta-period.svg)](https://github.com/SKY-ALIN/regta-period/blob/main/LICENSE)

### Moment-independence explanation

This term in this context means that relying on this approach we can get the time to time 
points regardless of the points in which we are.
```
         |-----------------|
         t1       t2     moment
---------|--------|--------|--------> time
                  |--------|
```

Whereas with normal intervals like `datetime.timedelta`, we get an unnecessary offset:
```
         |-----------------|
         t1       t2     moment
---------|--------|--------|--------|--------> time
                  |-----------------|
```

For example, it is important in the context of the job scheduler, because when the
scheduler is redeployed or restarted, you can get an unnecessary time shift or
unnecessary execution of the job.

### Math explanation of moment-independence

Essentially, it works as a remainder of the time division from the Unix epoch.
Let $t_{unix}$ be the moment of the Unix epoch, a moment that we can get a grip on.
$t$ is the current moment. Then, time since epoch is:

$$\ \Delta t = t - t_{unix} $$

Let $T$ be our period. Thus, to calculate time until the next moment we must subtract
from our period the remainder of the division by the period. Final function to calculate
time until the next moment since current looks following:

$$\ f(t) = T - ( \Delta t \mod T ) = T - ( ( t - t_{unix} ) \mod T ) $$

### Installation

Install using `pip install regta-period` or `poetry add regta-period`

---

Full documentation and reference are available at 
[regta-period.alinsky.tech](https://regta-period.alinsky.tech)
