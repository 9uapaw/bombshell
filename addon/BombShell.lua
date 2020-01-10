local A, T = ...

local dataStorage = {playerHp="-1", playerMana="-1", x="0", y="0", facing="0", playerState="000000", targetHp="-1", targetState="0", targetId="-1"}
local frameStorage = {playerHp=nil, playerMana=nil, xInt=nil, xDec=nil, yInt=nil, yDec=nil, facing=nil, playerState=nil, targetHp=nil, targetState=nil, targetId1=nil, targetId2=nil, targetId3=nil}

PLAYER_STATE = {combat=1, casting=2, last_ability=3, inventory=4, hasPet=5, firstResource=6}
TARGET_STATE = {distance=1}

BOX_SIZE = 5
MAX_COUNT_IN_ROW = 20

frame = CreateFrame("Frame", "MainFrame", UIParent)

function init() 
  local count = 0

  for k, v in ipairs(frameStorage) do
    local heightFromCorner = 0
    if (count > MAX_COUNT_IN_ROW) then
      heightFromCorner = math.floor(count / MAX_COUNT_IN_ROW) 
    end

    local frame = CreateFrame(k, "MainFrame", UIParent)
    frame:ClearAllPoints()
    frame:SetPoint("LEFT", 0, heightFromCorner)
    frame:SetHeight(BOX_SIZE)
    frame:SetWidth(BOX_SIZE)
    frame.texture = frame:CreateTexture(nil, "BACKGROUND")
    frame.texture:SetAllPoints(true)
    frame.texture:SetColorTexture(1, 1, 1, 1)
    frame:Show()

    frameStorage[key] = frame
  end
end

function StoreValue(key, value) 
    dataStorage[key] = value
end

function SetColor(key, rgb)
  frameStorage[key].texture:SetColorTexture(rgb["r"], rgb["g"], rgb["b"], 1)
end

function ValueToNormalizedRGB(unit, value)
  if unit == 'percentage' then
    return T.ToNormalizedRGB(T.ToRGB(T.ToHex(value, 10)))
  elseif unit == 'state' then
    return T.ToNormalizedRGB(T.ToRGB(T.ToHex(new, 16)))
  elseif unit == 'coordinate' then
    return T.FloatToNormalizedRGBPairs(value)
  elseif unit == "facing" then
    return T.FloatToNormalizedRGB(value)
  elseif unit == "id" then
    if value == "-1" then
      rgbs = {part1={1, 1, 1}, part2={1, 1, 1}, part3={1, 1, 1}}
      return rgbs
    end

    local part1 = ToNormalizedRGB(string.sub(value, 1, 6))
    local part2 = ToNormalizedRGB(string.sub(value, 7, 12))
    local part3 = ToNormalizedRGB(string.sub(value, 13, 18))
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
    StoreValue("playerState", val)
end

function SetTargetState(attr, val)
    local current = dataStorage["targetState"]

    if (not current) then
        current = string.rep("0", table.getn(TARGET_STATE))
    end

    local new = replace_char(TARGET_STATE[attr], current, val)
    local rgb = ValueToNormalizedRGB("state", new)

    SetColor("targetState", rgb)
    StoreValue("targetState", val)
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
  SetColor("playerHealth", ValueToNormalizedRGB(val))
  StoreValue("playerHealth", val)
end

function SetPlayerMana(val)
  SetColor("playerMana", ValueToNormalizedRGB(val))
  StoreValue("playerMana", val)
end

function SetTargetHealth(val)
  SetColor("targetHealth", ValueToNormalizedRGB(val))
  StoreValue("targetHealth", val)
end

function SetCoordinates(x, y)
  local xInt, xDec = ValueToNormalizedRGB(x)
  local yInt, yDec = ValueToNormalizedRGB(y)

  SetColor("xInt", xInt)
  SetColor("xDec", xDec)
  SetColor("yInt", yInt)
  SetColor("yDec", yDec)

  StoreValue("x", x)
  StoreValue("y", y)

end

function SetFacing(val)
  SetColor("facing", ValueToNormalizedRGB(val))
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


DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
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
            frame.text:SetText("" .. GetPlayerHealth())
            frame.mana:SetText("" .. GetPlayerMana())
            SetPlayerState("combat", "0")
            SetPlayerState("last_ability", "0")
            SetTargetState("distance", "0")
            SetPlayerState("inventory",  IsInventoryFull())
            SetPlayerState("hasPet",  IsPetExist())
            SetPlayerState("firstResource", IsFirstClassResourceAvailable())
            SetTargetHealth(GetTargetHealth())
            SetTargetGuid()
        elseif (event == "UNIT_HEALTH") then
            local health = GetPlayerHealth()
            local targetHealth = GetTargetHealth()
            SetPlayerHealth(health)
            SetTargetHealth(targetHealth)
        elseif (event == "UNIT_POWER_UPDATE") then
            local mana = GetPlayerMana()
            SetPlayerMana(mana)
        elseif (event == "PLAYER_REGEN_ENABLED") then
            SetPlayerState("combat", "0")
        elseif (event == "PLAYER_REGEN_DISABLED") then
            SetPlayerState("combat", "1")
        elseif (event == "PLAYER_TARGET_CHANGED") then
            local tuid = UnitLevel("target")
            local targetHealth = GetTargetHealth()
            local distance = GetTargetDistance()
            SetTargetState("distance", distance)
            SetTargetHealth(targetHealth)
            if targetHealth == -1 then
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
