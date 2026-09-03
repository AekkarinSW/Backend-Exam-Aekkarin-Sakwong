"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:
    _DIGIT_WORDS = (
        "ศูนย์",
        "หนึ่ง",
        "สอง",
        "สาม",
        "สี่",
        "ห้า",
        "หก",
        "เจ็ด",
        "แปด",
        "เก้า",
    )
    _POSITION_WORDS = ("", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน")
    _MILLION = 1_000_000

    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"

        if number == 0:
            return self._DIGIT_WORDS[0]

        if number < self._MILLION:
            return self._read_below_million(number)

        million_part, remainder = divmod(number, self._MILLION)
        result = f"{self._read_below_million(million_part)}ล้าน"

        if remainder:
            result += self._read_below_million(
                remainder,
                has_higher_part=True,
            )

        return result

    def _read_below_million(
        self,
        number: int,
        has_higher_part: bool = False,
    ) -> str:
        digits = str(number)
        number_of_digits = len(digits)
        words: list[str] = []

        for index, digit_text in enumerate(digits):
            digit = int(digit_text)

            if digit == 0:
                continue

            position = number_of_digits - index - 1

            if position == 0:
                if digit == 1 and (
                    number_of_digits > 1 or has_higher_part
                ):
                    words.append("เอ็ด")
                else:
                    words.append(self._DIGIT_WORDS[digit])
            elif position == 1:
                if digit == 1:
                    words.append("สิบ")
                elif digit == 2:
                    words.append("ยี่สิบ")
                else:
                    words.append(f"{self._DIGIT_WORDS[digit]}สิบ")
            else:
                words.append(
                    f"{self._DIGIT_WORDS[digit]}"
                    f"{self._POSITION_WORDS[position]}"
                )

        return "".join(words)


if __name__ == "__main__":
    solution = Solution()

    # Simple tests
    print("101 ->", solution.number_to_thai(101))
    print("21 ->", solution.number_to_thai(21))
    print("1,000,001 ->", solution.number_to_thai(1_000_001))
    print("-1 ->", solution.number_to_thai(-1))
