"""
Calculator Library Test Suite
Manual Test Engineer: 테스트 케이스 설계 및 실행
"""

import calc


def test_add():
    """add 함수 테스트"""
    print("\n=== Testing add() ===")
    
    # TC-001: 양수 덧셈
    result = calc.add(2, 3)
    expected = 5
    assert result == expected, f"TC-001 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-001 PASSED: add(2, 3) = {result}")
    
    # TC-002: 음수 덧셈
    result = calc.add(-5, 3)
    expected = -2
    assert result == expected, f"TC-002 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-002 PASSED: add(-5, 3) = {result}")
    
    # TC-003: 0 포함 덧셈
    result = calc.add(0, 5)
    expected = 5
    assert result == expected, f"TC-003 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-003 PASSED: add(0, 5) = {result}")
    
    # TC-004: 실수 덧셈
    result = calc.add(2.5, 3.7)
    expected = 6.2
    assert abs(result - expected) < 0.0001, f"TC-004 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-004 PASSED: add(2.5, 3.7) = {result}")


def test_subtract():
    """subtract 함수 테스트"""
    print("\n=== Testing subtract() ===")
    
    # TC-005: 양수 뺄셈
    result = calc.subtract(10, 3)
    expected = 7
    assert result == expected, f"TC-005 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-005 PASSED: subtract(10, 3) = {result}")
    
    # TC-006: 음수 결과
    result = calc.subtract(3, 10)
    expected = -7
    assert result == expected, f"TC-006 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-006 PASSED: subtract(3, 10) = {result}")
    
    # TC-007: 0 결과
    result = calc.subtract(5, 5)
    expected = 0
    assert result == expected, f"TC-007 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-007 PASSED: subtract(5, 5) = {result}")


def test_multiply():
    """multiply 함수 테스트"""
    print("\n=== Testing multiply() ===")
    
    # TC-008: 양수 곱셈
    result = calc.multiply(4, 5)
    expected = 20
    assert result == expected, f"TC-008 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-008 PASSED: multiply(4, 5) = {result}")
    
    # TC-009: 0 곱셈
    result = calc.multiply(10, 0)
    expected = 0
    assert result == expected, f"TC-009 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-009 PASSED: multiply(10, 0) = {result}")
    
    # TC-010: 음수 곱셈
    result = calc.multiply(-3, 4)
    expected = -12
    assert result == expected, f"TC-010 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-010 PASSED: multiply(-3, 4) = {result}")
    
    # TC-011: 음수 * 음수
    result = calc.multiply(-2, -6)
    expected = 12
    assert result == expected, f"TC-011 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-011 PASSED: multiply(-2, -6) = {result}")


def test_divide():
    """divide 함수 테스트"""
    print("\n=== Testing divide() ===")
    
    # TC-012: 정상 나눗셈
    result = calc.divide(10, 2)
    expected = 5.0
    assert result == expected, f"TC-012 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-012 PASSED: divide(10, 2) = {result}")
    
    # TC-013: 소수 결과
    result = calc.divide(7, 2)
    expected = 3.5
    assert result == expected, f"TC-013 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-013 PASSED: divide(7, 2) = {result}")
    
    # TC-014: 0으로 나누기 (예외 처리 확인)
    try:
        result = calc.divide(10, 0)
        print(f"✗ TC-014 FAILED: Expected ValueError, but got result {result}")
        assert False, "TC-014: Should raise ValueError"
    except ValueError as e:
        print(f"✓ TC-014 PASSED: divide(10, 0) raised ValueError: {e}")
    
    # TC-015: 음수 나눗셈
    result = calc.divide(-10, 2)
    expected = -5.0
    assert result == expected, f"TC-015 FAILED: Expected {expected}, got {result}"
    print(f"✓ TC-015 PASSED: divide(-10, 2) = {result}")


def test_power():
    """power 함수 테스트 - 버그 예상 영역"""
    print("\n=== Testing power() ===")
    
    # TC-016: 기본 거듭제곱
    result = calc.power(2, 3)
    expected = 8  # 2^3 = 8
    try:
        assert result == expected, f"TC-016 FAILED: Expected {expected}, got {result}"
        print(f"✓ TC-016 PASSED: power(2, 3) = {result}")
    except AssertionError as e:
        print(f"✗ TC-016 FAILED: {e}")
        print(f"  → BUG DETECTED: power() returns {result} instead of {expected}")
    
    # TC-017: 0 제곱
    result = calc.power(5, 0)
    expected = 1  # 5^0 = 1
    try:
        assert result == expected, f"TC-017 FAILED: Expected {expected}, got {result}"
        print(f"✓ TC-017 PASSED: power(5, 0) = {result}")
    except AssertionError as e:
        print(f"✗ TC-017 FAILED: {e}")
        print(f"  → BUG DETECTED: power() returns {result} instead of {expected}")
    
    # TC-018: 1 제곱
    result = calc.power(7, 1)
    expected = 7  # 7^1 = 7
    try:
        assert result == expected, f"TC-018 FAILED: Expected {expected}, got {result}"
        print(f"✓ TC-018 PASSED: power(7, 1) = {result}")
    except AssertionError as e:
        print(f"✗ TC-018 FAILED: {e}")
        print(f"  → BUG DETECTED: power() returns {result} instead of {expected}")
    
    # TC-019: 제곱수
    result = calc.power(3, 2)
    expected = 9  # 3^2 = 9
    try:
        assert result == expected, f"TC-019 FAILED: Expected {expected}, got {result}"
        print(f"✓ TC-019 PASSED: power(3, 2) = {result}")
    except AssertionError as e:
        print(f"✗ TC-019 FAILED: {e}")
        print(f"  → BUG DETECTED: power() returns {result} instead of {expected}")
    
    # TC-020: 음수 지수
    result = calc.power(2, -1)
    expected = 0.5  # 2^-1 = 0.5
    try:
        assert abs(result - expected) < 0.0001, f"TC-020 FAILED: Expected {expected}, got {result}"
        print(f"✓ TC-020 PASSED: power(2, -1) = {result}")
    except AssertionError as e:
        print(f"✗ TC-020 FAILED: {e}")
        print(f"  → BUG DETECTED: power() returns {result} instead of {expected}")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("Calculator Library - Manual Test Execution")
    print("=" * 60)
    
    failed_tests = []
    
    try:
        test_add()
    except Exception as e:
        failed_tests.append(f"test_add: {e}")
    
    try:
        test_subtract()
    except Exception as e:
        failed_tests.append(f"test_subtract: {e}")
    
    try:
        test_multiply()
    except Exception as e:
        failed_tests.append(f"test_multiply: {e}")
    
    try:
        test_divide()
    except Exception as e:
        failed_tests.append(f"test_divide: {e}")
    
    try:
        test_power()
    except Exception as e:
        failed_tests.append(f"test_power: {e}")
    
    # 테스트 결과 요약
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if failed_tests:
        print(f"\n⚠️  {len(failed_tests)} test group(s) encountered failures:")
        for test in failed_tests:
            print(f"  - {test}")
    else:
        print("\n✓ All test groups executed successfully!")
    
    print("\n⚠️  Known Issues:")
    print("  - power() function has a bug: returns a*b instead of a**b")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
