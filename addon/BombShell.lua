local A, T = ...

local dataStorage = {playerHp="-1", playerMana="-1", x="0", y="0", facing="0", playerState="000000", targetHp="-1", targetState="000000", targetId="-1"}
local frameStorage = {playerResource=0, xInt=0, xDec=0, yInt=0, yDec=0, facing=0, playerState=0, targetHp=0, targetState=0, targetId1=0, targetId2=0, targetId3=0}

PLAYER_STATE = {combat=1, casting=2, last_ability=3, inventory=4, hasPet=5, firstResource=6}
TARGET_STATE = {distance=1}
COLOR_ORDER = {"playerResource", "xInt", "xDec", "yInt", "yDec", "facing", "playerState", "targetHp", "targetState", "targetId1", "targetId2", "targetId3"}

BOX_SIZE = 20
ANCHOR = "TOPLEFT"
MAX_COUNT_IN_ROW = 20

frame = CreateFrame("Frame", "MainFrame", UIParent)
frame:SetPoint("TOPLEFT", 0, 0)

function init() 
  local count = 0
  local x = 0
  for i, k in ipairs(COLOR_ORDER) do
    local heightFromCorner = 0
    if (count > MAX_COUNT_IN_ROW) then
      heightFromCorner = math.floor(count / MAX_COUNT_IN_ROW) 
    end

    local frame = CreateFrame("Frame", k, UIParent)
    frame:ClearAllPoints()
    frame:SetPoint("TOPLEFT", x, heightFromCorner)
    frame:SetHeight(BOX_SIZE)
    frame:SetWidth(BOX_SIZE)
    frame.texture = frame:CreateTexture(nil, "BACKGROUND")
    frame.texture:SetAllPoints(true)
    frame.texture:SetColorTexture(1, 1, 1, 1)
    frame:Show()

    frameStorage[k] = frame

    x = x + BOX_SIZE
    count = count + 1
  end

  dataStorage["playerHp"] = "100"
  dataStorage["playerMana"] = "100"

end

function StoreValue(key, value)
    dataStorage[key] = value
end

function SetColor(key, rgb)
    if key == "playerResource" then
      print("SET COLOR: ", key, rgb["r"], rgb["g"], rgb["b"])
    end
    frameStorage[key].texture:SetColorTexture(rgb["r"], rgb["g"], rgb["b"], 1)
end

function ValueToNormalizedRGB(unit, value)
  if unit == 'percentage' then
    return T.ToNormalizedRGB(T.ToRGB(T.ToHex(value, 10)))
  elseif unit == 'playerResource' then
    print(value)
    local rgb = T.ToHPManaRGB(value)
    print("Player RGB: ", rgb["r"], rgb["g"], rgb["b"])
    local normalizedRgb = T.ToNormalizedRGB(rgb)
    print("Player Normalized RGB: ", normalizedRgb["r"], normalizedRgb["g"], normalizedRgb["b"])
    return normalizedRgb
  elseif unit == 'state' then
    return T.ToNormalizedRGB(T.ToRGB(T.ToHex(value, 16)))
  elseif unit == 'coordinate' then
    return T.FloatToNormalizedRGBPairs(value)
  elseif unit == "facing" then
    return T.FloatToNormalizedRGB(value)
  elseif unit == "id" then
    if value == "-1" then
      rgbs = {{r=1, g=1, b=1}, {r=1, g=1, b=1}, {r=1, g=1, b=1}}
      return rgbs
    end

    local hex1 = T.ToHex(string.sub(value, 1, 6), 16)
    local hex2 = T.ToHex(string.sub(value, 7, 12), 16)
    local hex3 = T.ToHex(string.sub(value, 13, 18), 16)

    local part1 = ToNormalizedRGB(ToRGB(hex1))
    local part2 = ToNormalizedRGB(ToRGB(hex2))
    local part3 = ToNormalizedRGB(ToRGB(hex3))
    local rgbs = {part1, part2, part3}
    return rgbs
  end
end

-- HELPER FUNCTIONS --
starts_with = T.starts_with
split = T.split
replace_char = T.replace_char

-- END OF HELPER FUNCTIONS --

function SetPlayerState(attr, val)
    local current = dataStorage["playerState"]

    if (not current) then
        current = string.rep("0", table.getn(PLAYER_STATE))
    end

    local new = replace_char(PLAYER_STATE[attr], current,val)
    local rgb = ValueToNormalizedRGB("state", new)

    SetColor("playerState", rgb)
    StoreValue("playerState", new)
end

function SetTargetState(attr, val)
    local current = dataStorage["targetState"]

    if (not current) then
        current = string.rep("0", 6)
    end

    local new = replace_char(TARGET_STATE[attr], current, val)
    local rgb = ValueToNormalizedRGB("state", new)

    SetColor("targetState", rgb)
    StoreValue("targetState", new)
end

function SetTargetGuid()
    local guid = UnitGUID("target")
    local target = GetTargetHealth()
    local new = "-1"
    if not guid or target == -1 then
      new = "-1"
    else
      guid = split(guid, "-")
      new = guid[6] .. guid[7]
    end

    local rgb = ValueToNormalizedRGB("id", new)
    SetColor("targetId1", rgb[1])
    SetColor("targetId2", rgb[2])
    SetColor("targetId3", rgb[3])

    StoreValue("targetId", new)
end

function SetPlayerHealth(val)
  local resource = dataStorage["playerMana"]
  local hexrep = string.sub(T.ToHex(val), -3)
  local new = hexrep .. string.sub(T.ToHex(resource), -3)

  print("MANA:" .. resource .. "HEX: " .. new)

  SetColor("playerResource", ValueToNormalizedRGB("playerResource", new))
  StoreValue("playerHp", val)
end

function SetPlayerMana(val)
  local resource = dataStorage["playerHp"]
  local hexrep = string.sub(T.ToHex(val) , -3)
  local new = string.sub(T.ToHex(resource), -3) .. hexrep

  print("HP:" .. resource .. "HEX: " .. new)

  SetColor("playerResource", ValueToNormalizedRGB("playerResource", new))
  StoreValue("playerMana", val)
end

function SetTargetHealth(val)
  SetColor("targetHp", ValueToNormalizedRGB("percentage", val))
  StoreValue("targetHp", val)
end

function SetCoordinates(x, y)
  local rgbX = ValueToNormalizedRGB("coordinate", x)
  local rgbY  = ValueToNormalizedRGB("coordinate", y)

  SetColor("xInt", rgbX[1])
  SetColor("xDec", rgbX[2])
  SetColor("yInt", rgbY[1])
  SetColor("yDec", rgbY[2])

  StoreValue("x", x)
  StoreValue("y", y)

end

function SetFacing(val)
  SetColor("facing", ValueToNormalizedRGB("facing", val))
  StoreValue("facing", val)
end

function GetPlayerHealth()
    local max = UnitHealthMax("player")
    local perc = floor(UnitHealth("player") / max * 100)

    return perc
end

function GetPlayerMana()
    local max = UnitPowerMax("player")
    local perc = floor(UnitPower("player") / max * 100)

    return perc
end

function GetTargetHealth()
    local max = UnitHealthMax("target")
    if max == 0 then
        return -1
    end
    local perc = floor(UnitHealth("target") / max * 100)

    return perc
end

function GetTargetDistance()
    local distance = 0
    if (CheckInteractDistance("target", 3)) then
                distance = 1
            elseif (CheckInteractDistance("target", 4)) then
                distance = 2
    end

    return distance
end

function GetSpellState()
    local info = {CombatLogGetCurrentEventInfo()}
            --DEFAULT_CHAT_FRAME:AddMessage("COMBAT LOG " .. info[2] .. " " .. info[4] .. " " ..info[15] )
    if (info[2] == 'SPELL_CAST_FAILED' and starts_with(info[4], 'Player')) then
        if (info[15] == "SPELL_FAILED_TOO_CLOSE") then
            return 3
        elseif (info[15] == "Target not in line of sight") then
            return 2
        elseif (info[15] == "Out of range") then
            return 1
        elseif (info[15] == "SPELL_FAILED_NOT_BEHIND") then
            return 4
        elseif (info[15] == "Target needs to be in front of you") then
            return 5
        elseif (info[15] == "SPELL_FAILED_BAD_IMPLICIT_TARGETS") then
            return 6
        end

    end

    return 0
end

function IsFirstClassResourceAvailable()
    local soulShards = GetItemCount("Soul Shard")
    local available = 0

    if soulShards > 0 then
        available = 1
    end

    return available
end

function GetPlayerCastingState()
    local spell, _, _, _, _, endTime = CastingInfo()
    local ret = 0
    if spell then
        ret = 1
    end

    return ret
end

function IsPetExist()
    local petSpells, _ = HasPetSpells()

    if petSpells == nil then
        return 0
    end

    return 1

end

function GetFacing()
    return GetPlayerFacing()
end

function IsInventoryFull()
    local freeSlots = 0
    for bagId=0,4 do
        numSlots, bagType = GetContainerNumFreeSlots(bagId)
        if bagType == 0 then
            freeSlots = freeSlots + numSlots
        end
    end

    local isFull = 0

    if freeSlots == 0 then
        isFull = 1
    end

    return isFull
end

function GetTruePosition()
    local mapID = C_Map.GetBestMapForUnit("player")
    local map = WorldMapFrame.ScrollContainer
    local width = map:GetWidth()
    local height = map:GetHeight()

	if mapID then
		local mapPos = C_Map.GetPlayerMapPosition(mapID, "player")
        if mapPos then
            local x, y = mapPos:GetXY()
            return x * width, y * height
        end
		end

    return -1, -1
end


frame:RegisterEvent("UNIT_HEALTH")
frame:RegisterEvent("UNIT_POWER_UPDATE")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PLAYER_REGEN_DISABLED")
frame:RegisterEvent("PLAYER_REGEN_ENABLED")
frame:RegisterEvent("PLAYER_TARGET_CHANGED")
frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
frame:RegisterEvent("LOOT_CLOSED")
frame:RegisterEvent("UNIT_PET")

frame:SetScript(
    "OnEvent",
    function(self, event, ...)
        if (event == "PLAYER_ENTERING_WORLD") then
            DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
            SetPlayerState("combat", "0")
            SetPlayerState("last_ability", "0")
            SetTargetState("distance", "0")
            SetPlayerState("inventory",  IsInventoryFull())
            SetPlayerState("hasPet",  IsPetExist())
            SetPlayerState("firstResource", IsFirstClassResourceAvailable())
            SetTargetHealth(GetTargetHealth())
            SetPlayerHealth(GetPlayerHealth())
            SetPlayerMana(GetPlayerMana())
            SetTargetGuid()
        elseif (event == "UNIT_HEALTH") then
            local health = GetPlayerHealth()
            local targetHp = GetTargetHealth()
            SetPlayerHealth(health)
            SetTargetHealth(targetHp)
        elseif (event == "UNIT_POWER_UPDATE") then
            local mana = GetPlayerMana()
            SetPlayerMana(mana)
        elseif (event == "PLAYER_REGEN_ENABLED") then
            SetPlayerState("combat", "0")
        elseif (event == "PLAYER_REGEN_DISABLED") then
            SetPlayerState("combat", "1")
        elseif (event == "PLAYER_TARGET_CHANGED") then
            local tuid = UnitLevel("target")
            local targetHp = GetTargetHealth()
            local distance = GetTargetDistance()
            SetTargetState("distance", distance)
            SetTargetHealth(targetHp)
            if targetHp == -1 then
                SetTargetGuid("-1")
            else
                SetTargetGuid()
            end
        elseif (event == "COMBAT_LOG_EVENT_UNFILTERED") then
            SetPlayerState("last_ability",  GetSpellState())
        elseif (event == "LOOT_CLOSED") then
            SetPlayerState("inventory",  IsInventoryFull())
        elseif (event == "UNIT_PET") then
            SetPlayerState("hasPet",  IsPetExist())
        end
    end
)

frame:SetScript(
    "OnUpdate",
    function(self, event)
        local posX, posY = GetTruePosition()
        local distance = GetTargetDistance()

        local facing = "" .. string.sub(GetFacing(), 0, 8)

        SetCoordinates(posX, posY)
        SetFacing(facing)
        SetPlayerState("casting", GetPlayerCastingState())
        SetTargetState("distance", distance)
        SetPlayerState("firstResource", IsFirstClassResourceAvailable())
    end
)

init()
frame:Show()
