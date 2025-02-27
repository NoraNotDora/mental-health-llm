package com.mentalhealth.project.system.result.service;

import com.mentalhealth.project.system.result.domain.ScaleResult;

import java.util.List;

/**
 * 测评结果参考信息Service接口
 * 
 * @author wzxy
 * @date 2021-10-28
 */
public interface IScaleResultService 
{
    /**
     * 查询测评结果参考信息
     * 
     * @param resultId 测评结果参考信息主键
     * @return 测评结果参考信息
     */
    public ScaleResult selectScaleResultByResultId(Long resultId);
    public ScaleResult selectScaleResultByScaleId(Long scaleId) ;

    /**
     * 查询测评结果参考信息列表
     * 
     * @param scaleResult 测评结果参考信息
     * @return 测评结果参考信息集合
     */
    public List<ScaleResult> selectScaleResultList(ScaleResult scaleResult);

    /**
     * 新增测评结果参考信息
     * 
     * @param scaleResult 测评结果参考信息
     * @return 结果
     */
    public int insertScaleResult(ScaleResult scaleResult);

    /**
     * 修改测评结果参考信息
     * 
     * @param scaleResult 测评结果参考信息
     * @return 结果
     */
    public int updateScaleResult(ScaleResult scaleResult);

    /**
     * 批量删除测评结果参考信息
     * 
     * @param resultIds 需要删除的测评结果参考信息主键集合
     * @return 结果
     */
    public int deleteScaleResultByResultIds(String resultIds);

    /**
     * 删除测评结果参考信息信息
     * 
     * @param resultId 测评结果参考信息主键
     * @return 结果
     */
    public int deleteScaleResultByResultId(Long resultId);
}
