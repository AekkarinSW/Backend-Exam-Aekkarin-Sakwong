"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:
    _ROMAN_VALUES = (
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )

    def number_to_roman(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"

        remaining = number
        roman_parts: list[str] = []

        for value, symbol in self._ROMAN_VALUES:
            count, remaining = divmod(remaining, value)
            if count:
                roman_parts.append(symbol * count)

        return "".join(roman_parts)


if __name__ == "__main__":
    solution = Solution()

    # Simple tests
    print("101 ->", solution.number_to_roman(101))  
    print("1994 ->", solution.number_to_roman(1994))
    print("-1 ->", solution.number_to_roman(-1))    
