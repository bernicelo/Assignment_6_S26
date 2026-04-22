
import re
import string


class InvalidPhoneNumber(Exception):
    pass


class PhoneNumber:

    def __init__(self, number='0000000000'):
        number_without_punctuation = PhoneNumber.strip_punctuation(number)

        if PhoneNumber.is_valid(number_without_punctuation):
            self._number = number_without_punctuation
        else:
            raise InvalidPhoneNumber(
                f"The Phone Number you have provided, "
                f" {number_without_punctuation} is not a valid US Number"
            )

    def get_raw_number(self):
        return self._number

    def set_raw_number(self, number):
        number_without_punctuation = PhoneNumber.strip_punctuation(number)

        if PhoneNumber.is_valid(number_without_punctuation):
            self._number = number_without_punctuation
        else:
            raise InvalidPhoneNumber(
                f"The Phone Number you have provided, "
                f" {number_without_punctuation} is not a valid US Number"
            )

    def get_area_code(self):
        return self._number[0:3]

    def set_area_code(self, area_code):
        if len(area_code) == 3:
            self._number = area_code + self._number[3:]
            if not PhoneNumber.is_valid(self._number):
                raise InvalidPhoneNumber(
                    f"The Phone Number "
                    f" {self._number} is not a valid US Number"
                )
        else:
            raise InvalidPhoneNumber(
                f"The area code is not the correct length "
                f"to give a valid phone number."
            )

        print(self._number)

    def get_exchange(self):
        return self._number[3:6]

    def set_exchange(self, exchange_number):
        if len(exchange_number) == 3:
            self._number = (
                self._number[0:3] + exchange_number + self._number[6:]
            )
        else:
            raise InvalidPhoneNumber(
                f"The exchange number is not the correct "
                f"length to get valid phone number."
            )

    def get_subscriber_number(self):
        return self._number[6:]

    def set_subscriber_number(self, subscriber_number):
        if len(subscriber_number) == 4:
            self._number = self._number[:6] + subscriber_number
        else:
            raise InvalidPhoneNumber(
                f"The subscriber number is not the correct "
                f"length to get valid phone number."
            )

    def get_formatted_number(self):
        return (
            f'({self.get_area_code()}) '
            f'{self.get_exchange()}-{self.get_subscriber_number()}'
        )

    def __str__(self):
        return self.get_formatted_number()

    def __ge__(self, other):
        if isinstance(other, PhoneNumber):
            return self._number >= other._number

    def __le__(self, other):
        if isinstance(other, PhoneNumber):
            return self._number <= other._number

    def __eq__(self, other):
        if isinstance(other, PhoneNumber):
            return self._number == other._number

    def __gt__(self, other):
        if isinstance(other, PhoneNumber):
            return self._number > other._number

    def __lt__(self, other):
        if isinstance(other, PhoneNumber):
            return self._number < other._number

    @staticmethod
    def strip_punctuation(number):
        return number.translate(
            str.maketrans("", "",  string.punctuation + string.whitespace)
        )

    @staticmethod
    def is_valid(number_to_check):
        '''
        takes as input a number, which is string.
        before calling this function, all punctuation is stripped so
        it should just be a string of numbers
        returns True if the number is a valid (US) number
        returns False if not
        '''
        # first we make sure it's a string of digits
        if (
            not isinstance(number_to_check, str) or
            not number_to_check.isdigit()
        ):
            return False
        # then we make sure it's the right length
        if len(number_to_check) == 11:
            if number_to_check[0] == '1':
                number_to_check = number_to_check[1:]
                # if it has a leading 1, we trim it off
            else:
                # number must start with 1
                return False
        elif len(number_to_check) == 10:
            pass
        else:
            return False
        # at this point we know it's a string of length 10.
        # these will check if there are certain reserved
        # prefixes in the number that are not part of a valid number
        if re.match(r'^\d{10}$', number_to_check):
            if (
                re.match(r'^[2-9]9', number_to_check)
                or re.match(r'^37|96', number_to_check)
                or re.match(r'^[2-9]11', number_to_check)
            ):
                return False
            else:
                return True
