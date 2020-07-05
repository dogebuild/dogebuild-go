package lib

import "testing"

func TestGreet(t *testing.T) {
    expected := "Hello test!"
    actual := Greet("test")

    if expected != actual {
        t.Errorf("Expected %q but was %q", expected, actual)
    }
}
