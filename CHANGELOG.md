## 0.2.0 (28.12.2022)
* Add Python 3.11 support
* Add `AbstractPeriod.is_timezone_in_use`
* Add `Period.is_timezone_in_use`
* Add `PeriodAggregation.is_timezone_in_use`

## 0.1.0 (22.08.2022)
* Add `regta_period.AbstractPeriod`
  * `.get_next`
  * `.get_interval`
* Add `regta_period.Period`
  * `.every`
  * `.seconds`
  * `.minutes`
  * `.hours`
  * `.days`
  * `.hourly`
  * `.daily`
  * `.on`
  * `.monday`
  * `.tuesday`
  * `.wednesday`
  * `.thursday`
  * `.friday`
  * `.saturday`
  * `.sunday`
  * `.weekdays`
  * `.weekends`
  * `.at`
  * `.by`
  * `.get_next`
  * `.get_interval`
  * `.AND`
  * `.OR`
  * `.__add__`
  * `.__or__`
  * `.__repr__`
* Add `regta_period.PeriodAggregation`
  * `.get_next`
  * `.get_interval`
  * `.OR`
  * `.__or__`
  * `.__dir__`
  * `.__getattr__`
  * `.__repr__`
* Add `regta_period.Weekdays`
  * `.get`
