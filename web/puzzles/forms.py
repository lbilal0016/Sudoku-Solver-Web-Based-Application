from django import forms

class SudokuForm(forms.Form):
    puzzle = forms.CharField(
        min_length=81,
        max_length=81,
        label="Sudoku",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Please enter a sudoku puzzle in form of 81 digits",
                "autocomplete": "off",
            }
        )
    )

    def clean_puzzle(self):
        puzzle = self.cleaned_data["puzzle"]

        if any(character not in "0123456789" for character in puzzle):
            raise forms.ValidationError(
                "Please provide a sudoku which only consists of digits [0-9]"
            )
        
        return puzzle