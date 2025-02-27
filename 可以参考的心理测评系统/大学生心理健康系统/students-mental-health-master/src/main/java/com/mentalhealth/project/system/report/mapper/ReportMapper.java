package com.mentalhealth.project.system.report.mapper;

import com.mentalhealth.project.system.report.domain.Report;

import java.util.List;

/**
 * 举报信息Mapper接口
 * 
 * @author wzxy
 * @date 2021-11-20
 */
public interface ReportMapper 
{
    /**
     * 查询举报信息
     * 
     * @param reportId 举报信息主键
     * @return 举报信息
     */
    public Report selectReportByReportId(Long reportId);

    /**
     * 查询举报信息列表
     * 
     * @param report 举报信息
     * @return 举报信息集合
     */
    public List<Report> selectReportList(Report report);

    /**
     * 新增举报信息
     * 
     * @param report 举报信息
     * @return 结果
     */
    public int insertReport(Report report);

    /**
     * 修改举报信息
     * 
     * @param report 举报信息
     * @return 结果
     */
    public int updateReport(Report report);

    /**
     * 删除举报信息
     * 
     * @param reportId 举报信息主键
     * @return 结果
     */
    public int deleteReportByReportId(Long reportId);

    /**
     * 批量删除举报信息
     * 
     * @param reportIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteReportByReportIds(String[] reportIds);
}
