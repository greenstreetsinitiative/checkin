from django.utils import timezone
from datetime import date
from calendar import isleap

class Registration(object):
    friday = 4
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    @staticmethod
    def is_open(today=date.today()):
        """
        Boolean that determines if registration is open for new participants
        today is a datetime object.
        """
        current_year = today.year
        reg_open = date(year=current_year, month=1, day=1)
        reg_close =  date(year=current_year, month=4, day=15)
        return reg_open < today < reg_close


    @staticmethod
    def _days_in_month_(year, month):
        """ Returns number of days in a month given month and year """
        if month == 2 and isleap(year):
            return 29
        else:
            return LastFriday.days_per_month[month-1]

    @staticmethod
    def last_friday(year, month):
        """
        Returns the day of the month corresponding to the last Friday of that
        month given a year and a month
        """
        friday = LastFriday.friday
        num_days = LastFriday._days_in_month_(month, year)

        # Calculate first Friday of the month
        first_day = date(year, month, 1).weekday()
        if first_day <= friday:
            first_friday = 1 + friday - first_day
        else:
            first_friday = 8 - (first_day - friday)

        return first_friday + 7 * int((num_days - first_friday)/7)

    @staticmethod
    def deadline(month, year=date.today().year):
        day = Registration.last_friday(year, month)
        return timezone.datetime(year=year, month=month, day=day)

    @staticmethod
    def early_registration_multiplier(registration_date=timezone.now()):
        """
        Calculates price multiplier based on date

        Registration opens in January
        If you register before the last friday of January, you pay some fee x*
        If before the last friday of February, it's 1.1*x
        If before last friday of March, it's 1.1*1.1*x
        Registration close in April

        * The value of x depends on the size of the business and number of
          subteams
        """
        multiplier = 1
        for i in xrange(3):
            if i <= Registration.deadline(i+1, registration_date.year):
                return multiplier
            multiplier *= 1.1

    @staticmethod
    def size_fee(size):
        """
        Returns fee to be paid for a company of a certain size during the
        early bird discount period.

        Sorry for the endless if elses, but the pricing is seemingly arbitrary
        """
        if size > 5000:
            return 950
        elif size > 3000:
            return 850
        elif size > 1000:
            return 800
        elif size > 500:
            return 650
        elif size > 100:
            return 550
        elif size > 50:
            return 450
        elif size > 15:
            return 250
        elif size > 0:
            return 150
        else:
            return 0

    @staticmethod
    def subteam_fee(num_subteams):
        """ Calculates additional fee based on number of subteams """
        return 50 * num_subteams

    @staticmethod
    def fee(size, num_subteams=0, today=timezone.now()):
        """
        Given the size of a business, the number of subteams, registration
        date, and discount, determines the fee to be paid

        Inputs:
            size: integer representing number of employees
            num_subteams: number of subteams (defaults to no subteams)
            today: date of registration

        Output:
            fee in dollars
        """
        subteam_fee = Registration.subteam_fee(num_subteams) \
            if num_subteams > 0 else 0
        size_fee = Registration.size_fee(size)
        deadline_multiplier = Registration.early_registration_multiplier(today)
        return subteam_fee + deadline_multiplier * size_fee
