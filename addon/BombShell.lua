frame = CreateFrame("Frame", "MainFrame", UIParent)
frame:ClearAllPoints()
frame:SetHeight(600)
frame:SetWidth(320)

function replace_char(pos, str, r)
    return str:sub(1, pos-1) .. r .. str:sub(pos+1)
end

function SetPlayerState(attr, val)
    local current = frame.playerState:GetText()

    if (not current) then
        current = string.rep("0", table.getn(PLAYER_STATE))
    end

    frame.playerState:SetText(replace_char(PLAYER_STATE[attr], current,val))
    end

function SetTargetState(attr, val)
    local current = frame.targetState:GetText()

    if (not current) then
        current = string.rep("0", table.getn(TARGET_STATE))
    end

    frame.targetState:SetText(replace_char(TARGET_STATE[attr], current, val))
end

PARENT = "GameFontNormal"
FONT = "Interface\\AddOns\\BombShell\\data\\font\\default.ttf"
FONT_SIZE = 50
START = 30
LINE_SPACE = 30
DATA = {"text", "mana", "posx", "posy", "facing", "playerState", "targetHealth", "targetState" }
PLAYER_STATE = {combat=1, casting=2}
TARGET_STATE = {distance=1}

for k, v in ipairs(DATA) do
    local t = frame:CreateFontString(v, "BACKGROUND", PARENT)
    t:SetPoint("CENTER", 0, START - k * LINE_SPACE)
    t:SetJustifyH("LEFT")
    t:SetTextColor(0, 0, 0, 1)
    t:SetFont(FONT, FONT_SIZE)
    frame[v] = t
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
    local timestamp, subevent, _ = CombatLogGetCurrentEventInfo()
            DEFAULT_CHAT_FRAME:AddMessage("COMBAT LOG " .. subevent .. timestamp)
            if (subevent == "SPELL_FAILED_TOO_CLOSE") then
                return 3
            elseif (subevent == "SPELL_FAILED_LINE_OF_SIGHT") then
                return 2
            elseif (subevent == "SPELL_FAILED_OUT_OF_RANGE") then
                return 1
            elseif (subevent == "SPELL_FAILED_NOT_BEHIND") then
                return 4
            elseif (subevent == "SPELL_FAILED_UNIT_NOT_INFRONT") then
                return 5
            elseif (subevent == "SPELL_FAILED_BAD_IMPLICIT_TARGETS") then
                return 6
            end
end

function GetPlayerCastingState()
    local spell, _, _, _, _, endTime = CastingInfo()
    local ret = 0
    if spell then
        ret = 1
    end

    return ret
end

function GetFacing()
    return GetPlayerFacing()
end

function GetTruePosition()
    local mapID = C_Map.GetBestMapForUnit("player")

	if mapID then
		local mapPos = C_Map.GetPlayerMapPosition(mapID, "player")
        if mapPos then
            local x, y = mapPos:GetXY()
            return x * 100, y * 100
        end
		end

    return -1, -1
end

frame:SetPoint("LEFT", 0, 200)

frame:SetBackdrop(
    {
        insets = {left = 4, right = 4, top = 4, bottom = 4},
        backdropColor = {r = 1, g = 1, b = 1, a = 0}
    }
)
frame.texture = frame:CreateTexture(nil, "BACKGROUND")
frame.texture:SetAllPoints(true)
frame.texture:SetColorTexture(1, 1, 1, 1)

DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
frame:RegisterEvent("UNIT_HEALTH")
frame:RegisterEvent("UNIT_MANA")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PLAYER_REGEN_DISABLED")
frame:RegisterEvent("PLAYER_REGEN_ENABLED")
frame:RegisterEvent("PLAYER_TARGET_CHANGED")
frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")

frame:SetScript(
    "OnEvent",
    function(self, event, ...)
        if (event == "PLAYER_ENTERING_WORLD") then
            DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
            frame.text:SetText("" .. GetPlayerHealth())
            frame.mana:SetText("" .. GetPlayerMana())
            SetPlayerState("combat", "0")
            SetTargetState("distance", "0")
            frame.targetHealth:SetText("" .. -1)
--            frame.tuid:SetText("TID: " .. 0)
        elseif (event == "UNIT_HEALTH") then
            local health = GetPlayerHealth()
            local targetHealth = GetTargetHealth()
            frame.text:SetText("" .. health)
            frame.targetHealth:SetText("" .. targetHealth)
        elseif (event == "UNIT_MANA") then
            local mana = GetPlayerMana()
            frame.mana:SetText("" .. mana)
        elseif (event == "PLAYER_REGEN_ENABLED") then
            SetPlayerState("combat", "0")
        elseif (event == "PLAYER_REGEN_DISABLED") then
            SetPlayerState("combat", "1")
        elseif (event == "PLAYER_TARGET_CHANGED") then
            local tuid = UnitLevel("target")
            local targetHealth = GetTargetHealth()
            local distance = GetTargetDistance()
            SetTargetState("distance", distance)
            frame.targetHealth:SetText("" .. targetHealth)
--            frame.tuid:SetText("TID: " .. tuid)
        elseif (event == "COMBAT_LOG_EVENT_UNFILTERED") then
            --frame.ability:SetText("" .. GetSpellState())
        end
    end
)

frame:SetScript(
    "OnUpdate",
    function(self, event)
        local posX, posY = GetTruePosition()
        frame.posx:SetText("" .. string.sub(posX, 0, 8))
        frame.posy:SetText("" .. string.sub(posY, 0, 8))

        frame.facing:SetText("" .. string.sub(GetFacing(), 0, 8))

        SetPlayerState("casting", GetPlayerCastingState())
    end
)

frame:Show()
