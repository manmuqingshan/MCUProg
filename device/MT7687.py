from .flash import Flash


class MT7687(object):
    CHIP_CORE = 'Cortex-M4'

    PAGE_SIZE = 1024 * 1
    SECT_SIZE = 1024 * 4
    CHIP_SIZE = 0x400000    # 4MByte

    def __init__(self, xlink):
        super(MT7687, self).__init__()
        
        self.xlink = xlink

        self.flash = Flash(self.xlink, MT7687_flash_algo)

    def sect_erase(self, addr, size):
        self.flash.Init(0, 0, 1)
        for i in range(0, (size + self.SECT_SIZE - 1)//self.SECT_SIZE):
            self.flash.EraseSector(0x10000000 + addr + self.SECT_SIZE * i)
        self.flash.UnInit(1)

    def chip_write(self, addr, data):
        self.sect_erase(addr, len(data))

        self.flash.Init(0, 0, 2)
        for i in range(0, len(data)//self.PAGE_SIZE):
            self.flash.ProgramPage(0x10000000 + addr + self.PAGE_SIZE * i, data[self.PAGE_SIZE*i : self.PAGE_SIZE*(i+1)])
        self.flash.UnInit(2)

    def chip_read(self, addr, size, buff):
        # 必须按一下复位键，然后执行以下三条语句，才能从内存空间读到值
        self.xlink.write_U32(0x8300F050, 0x76371688)
        self.xlink.write_U32(0x8300F050, 0x76371688)
        self.xlink.write_U32(0x8300F050, 0x76371688)

        c_char_Array = self.xlink.read_mem(0x10000000 + addr, size)

        buff.extend(list(bytes(c_char_Array)))


MT7687_flash_algo = {
    'load_address' : 0x20000000,
    'instructions' : [
        0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
        0xEA412100, 0xF44F6210, 0xEA01417F, 0x43112110, 0x027FF44F, 0x2200EA02, 0xEA42430A, 0x47706000,
        0x68114AAA, 0x2801B110, 0xE006D002, 0xE0006850, 0x07C06C10, 0xF041D001, 0xF0410110, 0x6C500108,
        0xD5FC0480, 0x05C06890, 0x6011D5FC, 0x489F4770, 0x4A9F6801, 0x60014011, 0x07896801, 0x6801D4FC,
        0x0108F021, 0x68016001, 0xD4FC0709, 0x4A974770, 0x20004603, 0x2B016811, 0x010CF041, 0xF041D101,
        0x60115180, 0x07896811, 0x6811D5FC, 0xD1FC07C9, 0xB5104770, 0xF7FF4604, 0x4620FFEA, 0x4010E8BD,
        0xB530E7D5, 0x46052300, 0xE006461C, 0x460C4620, 0x1C5B0A09, 0x241FF360, 0x2900B2DB, 0x2B00D1F6,
        0x4628D00C, 0xFFACF7FF, 0x60044882, 0x6103487F, 0x61412100, 0xE8BD4628, 0xE7DA4030, 0xB530BD30,
        0x460C4605, 0xF7FF4610, 0x2B03FF8B, 0xEA44D012, 0x0E002200, 0x600A4977, 0x60081D09, 0x1C5B4873,
        0x21006103, 0x46286141, 0xFF8AF7FF, 0xE8BD4628, 0xE7BE4030, 0x02FFF020, 0xE7EB4322, 0x4603B500,
        0xF7FF4608, 0xF363FF6D, 0xBD000007, 0x4B69B538, 0x078B4418, 0x07CBD009, 0x466CD015, 0xDD062A00,
        0xE0192300, 0xC008C908, 0x2A001F12, 0xBD38DCFA, 0x3B02F831, 0x3000F8AD, 0x3B02F831, 0x3002F8AD,
        0xC0089B00, 0x2A001F12, 0xBD38DCF2, 0x5B01F811, 0x1C5B54E5, 0xD2012B04, 0xD3F74293, 0xC0089B00,
        0xE7DB1F12, 0x4DF8E92D, 0xF8DF4683, 0x461DA148, 0x20004616, 0x4652466B, 0x9F094680, 0x2400E00F,
        0x8000F8CD, 0xF811E005, 0xF803C000, 0x1C40C004, 0x42A81C64, 0x2C04D201, 0x9C00D3F5, 0x42A8C210,
        0x4842D3ED, 0x61476105, 0xF7FF4658, 0x4658FF29, 0xFF5FF7FF, 0xEB052000, 0xE004010A, 0x2B01F811,
        0x2B01F806, 0x42B81C40, 0xE8BDD3F8, 0xE92D8DF8, 0x000F4DFC, 0xF04F4680, 0xD0450500, 0x68704E33,
        0x0B01F000, 0x28015D78, 0x2802D00D, 0x2803D00B, 0xF1B8D014, 0xD02D0F00, 0xF1BB6C30, 0xD0350F00,
        0x0001F040, 0xF1B8E034, 0xD0030F00, 0xF0206C30, 0xE0090001, 0xF0206870, 0xE00A0001, 0x0F00F1B8,
        0x6C30D004, 0x0001F040, 0xE0036430, 0xF0406870, 0x60700001, 0x78A0197C, 0xD01B2805, 0x90002000,
        0x78634602, 0x46401CA1, 0xFF8CF7FF, 0x1CAD7860, 0xE7C74405, 0xF1BB6870, 0xD0020F00, 0x0001F040,
        0xF020E001, 0x60700001, 0x8DFCE8BD, 0x0001F020, 0xE7F96430, 0x0A01F04F, 0x23011CA1, 0x4640AA01,
        0xA000F8CD, 0xFF6EF7FF, 0xF89D78E0, 0x42081004, 0xE7DBD1F2, 0xB081B507, 0x93002303, 0x2301460A,
        0xF7FFA903, 0xBD0FFF5F, 0xE7F3229F, 0x83070000, 0xEFFFFFEB, 0x83070800, 0xB530487A, 0x44484978,
        0x22004449, 0x86CA6001, 0xF8812203, 0xF1012035, 0x23020244, 0x7013624A, 0x22066804, 0x70626A64,
        0x24C76802, 0x716C6A55, 0x24206A55, 0x6A5271AC, 0x74142405, 0x620A1D02, 0x70112101, 0x6A096801,
        0x6802704B, 0x6A122108, 0x68027091, 0x6A122104, 0x680070D1, 0x6A02213C, 0x6A027111, 0x71512180,
        0x21606A00, 0x200071C1, 0x2000BD30, 0xB5704770, 0x460D4604, 0xF7FF8EC0, 0x4E5BFE63, 0x485B6035,
        0x61012101, 0x8EE06141, 0xFE93F7FF, 0xF3C06830, 0xBD702007, 0x4C53B510, 0x6820444C, 0x7C096A41,
        0xFFE5F7FF, 0x6A096821, 0x42017809, 0xBD10D1F5, 0x4C4CB510, 0x6820444C, 0x8EC06A41, 0xF7FF7849,
        0x6820FE80, 0x8EC06A41, 0xF7FF7949, 0xF7FFFE7A, 0x2000FFE1, 0xB570BD10, 0xF7FF4605, 0x4C41FFDB,
        0x6823444C, 0x78416A58, 0xF7FF8ED8, 0xF7FFFE6A, 0x6824FFD1, 0x6A60462A, 0x3035F894, 0x8EE07981,
        0xFE7DF7FF, 0xFFC6F7FF, 0xBD702000, 0x41F0E92D, 0x46074D34, 0x460E444D, 0x24006828, 0x7C096A41,
        0xFFA5F7FF, 0xB2806829, 0x78096A09, 0xD1064201, 0x42B07838, 0x2401D101, 0xF04FE001, 0x462034FF,
        0x81F0E8BD, 0x47F0E92D, 0x460D4617, 0xF7FF4606, 0xE040FFA1, 0x007FF006, 0x0480F1C0, 0xD80042A5,
        0xF8DF462C, 0x44C88080, 0x0000F8D8, 0x8EC06A41, 0xF7FF7849, 0xF8D8FE26, 0x46310000, 0x78006A40,
        0xFE5CF7FF, 0x46224682, 0x20044639, 0xFE5EF7FF, 0xF8C14915, 0xF8D8A000, 0x1C610000, 0x2035F890,
        0x4912440A, 0x2200610A, 0x8EC0614A, 0xFDC8F7FF, 0x0000F8D8, 0xF7FF8EC0, 0xEB07FDFC, 0x44260804,
        0x1C01F818, 0xF7FF1E70, 0x2800FFA1, 0x1B2DD0F8, 0x28014427, 0x2D00D101, 0x2000D1BC, 0x87F0E8BD,
        0x00000010, 0x00000004, 0x83070800, 0x83070000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
        0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
        0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
        0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000
    ],

    'pc_Init'            : 0x200002F9,
    'pc_UnInit'          : 0x2000036B,
    'pc_EraseSector'     : 0x200003D7,
    'pc_ProgramPage'     : 0x20000445,
    'pc_Verify'          : 0x12000001F,
    'pc_EraseChip'       : 0x200003B1,
    'pc_BlankCheck'      : 0x12000001F,
    'pc_Read'            : 0x12000001F,
    
    'static_base'        : 0x200004F0,
    'begin_data'         : 0x20000558,
    'begin_stack'        : 0x20000D58,

    'analyzer_supported' : False,

    # Relative region addresses and sizes
    'ro_start'           : 0x00000000,
    'ro_size'            : 0x000004D0,
    'rw_start'           : 0x000004D0,
    'rw_size'            : 0x00000010,
    'zi_start'           : 0x000004E0,
    'zi_size'            : 0x00000058,

    # Flash information
    'flash_start'        : 0x10000000,
    'flash_size'         : 0x00400000,
    'flash_page_size'    : 0x00000400,
    'sector_sizes': (
        (0x00000, 0x01000),
    )
}
