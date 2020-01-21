local A, T = ...


local b = "10101010111000110"

function ToHex(number, base)
  if number == "-1" then
    return "FFFFFF"
  end

  local hex = number 
  if (base ~= 16) then
    hex = tonumber(number, base)
  else
    hex = tonumber(number, 16)
  end

  return string.format("%06x", hex)
end

function ToHPManaRGB(hex)
  local rgb = {r=0, g=0, b=0}

  rgb["r"] = tonumber(hex:sub(1, 2))
  rgb["g"] = tonumber(hex:sub(3, 4))
  rgb["b"] = tonumber(hex:sub(5, 6))

  return rgb
end

function ToRGB(hex)
  local rgb = {r=0, g=0, b=0}

  rgb["r"] = tonumber(hex:sub(1, 2))
  rgb["g"] = tonumber(hex:sub(3, 4))
  rgb["b"] = tonumber(hex:sub(5, 6))

  return rgb
end

function ToNormalizedRGB(rgb)
  rgb["r"] = rgb["r"] / 255
  rgb["g"] = rgb["g"] / 255
  rgb["b"] = rgb["b"] / 255

  return rgb
end

function FloatToNormalizedRGB(float)
  local intPart, decPart = string.match(tostring(float), "([^.]*)%.([^.]*)")

  local decPart = string.sub(decPart, 0, 6)
  local decHex = ToHex(decPart, 10)
  local fullHex = intPart..decHex

  return ToNormalizedRGB(ToRGB(fullHex))
end

function FloatToNormalizedRGBPairs(float)
  local intPart, decPart = string.match(tostring(float), "([^.]*)%.([^.]*)")

  local intHex = ToHex(intPart, 10)
  local decHex = ToHex(string.sub(decPart, 0, 6), 10)

  local rgbs = {}
  rgbs[1] = ToNormalizedRGB(ToRGB(intHex))
  rgbs[2] = ToNormalizedRGB(ToRGB(decHex))

  return rgbs
end

function starts_with(str, start)
   return str:sub(1, #start) == start
end

function split(s, delimiter)
    result = {};
    for match in (s..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match);
    end
    return result;
end

function replace_char(pos, str, r)
    return str:sub(1, pos-1) .. r .. str:sub(pos+1)
end

T.ToNormalizedRGB = ToNormalizedRGB
T.ToHex = ToHex
T.ToRGB = ToRGB
T.FloatToNormalizedRGBPairs = FloatToNormalizedRGBPairs
T.FloatToNormalizedRGB = FloatToNormalizedRGB
T.split = split
T.replace_char = replace_char
T.starts_with = starts_with
T.ToHPManaRGB = ToHPManaRGB

