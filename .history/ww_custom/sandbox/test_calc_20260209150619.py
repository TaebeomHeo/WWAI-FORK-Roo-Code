import { vi, describe, test, it } from 'vitest'
import { add, subtract, multiply, divide, power } from '../calc'

describe('Calculator functions', () => {
  it('should add numbers correctly', () => {
    expect(add(2, 3)).toBe(5)
    expect(add(-1, 1)).toBe(0)
    expect(add(0, 0)).toBe(0)
  })

  it('should subtract numbers correctly', () => {
    expect(subtract(5, 3)).toBe(2)
    expect(subtract(-1, 1)).toBe(-2)
    expect(subtract(0, 0)).toBe(0)
  })

  it('should multiply numbers correctly', () => {
    expect(multiply(2, 3)).toBe(6)
    expect(multiply(-1, 1)).toBe(-1)
    expect(multiply(0, 5)).toBe(0)
  })

  it('should divide numbers correctly', () => {
    expect(divide(6, 3)).toBe(2)
    expect(divide(-6, 3)).toBe(-2)
    expect(() => divide(6, 0)).toThrow('Cannot divide by zero')
  })

  it('should power numbers correctly', () => {
    expect(power(2, 3)).toBe(8)
    expect(power(2, -2)).toBe(0.25)
    expect(power(0, 5)).toBe(0)
    expect(() => power(0, -2)).toThrow('Cannot divide by zero')
    expect(power(-2, 3)).toBe(-8)
    expect(power(-2, 2)).toBe(4)
    expect(power(2, 0.5)).toBe(Math.sqrt(2))
  })
})
